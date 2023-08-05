import sys
import time

sys.path.append('../')

import datetime
import uuid
import random
import logging
from time import sleep
import pandas as pd

format = "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s() line: %(lineno)d: %(message)s"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    level=logging.INFO)


from Management import Management


class ExecutionBot(Management):

    def __init__(self, strategy, starting_money,
                 market_event_securities, market_event_queue, securities,
                 host=None, bot_id=None):

        super(ExecutionBot, self).__init__(strategy, starting_money,
                                        market_event_securities, market_event_queue, securities,
                                        host, bot_id)

        # # Subscription to order book in order to passively send orders
        # self.kickoff()

        # actively send orders
        self.start()

        # give some time for agent to receive queue in channel since it is 'direct' for now
        sleep(10)

    def aggressive_orders(self, qty, action, exec_t=2, log=False):

        sym = self.securities[0]

        book_side = 'Ask' if action == 'buy' else 'Bid'
        side = 'B' if action == 'buy' else 'S'

        # benchmark price
        benchmark_price = self.mid_market[sym]
        benchmark_vwap = self.vwap[sym]

        # target qty
        qty_target = qty

        # setup timer
        t_start = time.time()

        # pv = execution price * volume
        pv = 0

        # print(self.market_dict[sym])

        # sending aggressive orders til all qty becomes zero
        # It could be more than one loops due to price slippage
        while qty > 0 and time.time() - t_start < exec_t:

            # search the price level that covers all qty
            book_levels = self.market_event_queue.copy()

            # determine the order price/size to be executed
            size = 0
            order_prices = []
            order_qty = []
            while size < qty and len(book_levels) > 0:
                level = book_levels.pop(0)
                size_level = min(qty-size, self.market_dict[sym][level][book_side + 'Size'])
                size += int(size_level)

                order_prices.append(self.market_dict[sym][level][book_side + 'Price'])
                order_qty.append(size_level)

            # print(order_qty)

            # TODO: what if the whole book is insufficient? -> qty = size

            # send orders
            orders = []
            for p, q in zip(order_prices, order_qty):
                order = {'symb': sym,
                         'price': p,
                         'origQty': q,
                         'status': "A",
                         'remainingQty': q,
                         'action': "A",
                         'side': side,
                         'FOK': 0,
                         'AON': 0,
                         'strategy': self.strategy,
                         'orderNo': self.internalID
                         }

                self.send_order(order)
                logging.info(f"Aggressive order sent: \n"
                             f"\t {order['symb']}: "
                                     f"{order['orderNo']} | "
                                     f"{order['side']} | "
                                     f"{order['origQty']} | "
                                     f"{order['remainingQty']} | "
                                     f"{order['price']}")

                orders.append(order)
                self.internalID += 1

            # cancel orders
            qty = 0

            for order in orders:
                
                in_id = order["orderNo"]

                # make sure all orders are acked on matching enginee
                while in_id in self.inIds_to_orders_sent:
                    sleep(0.001)
                    # print(f'waiting for pending orders...')

                # cancel only if the order is not fully filled
                if in_id in self.inIds_to_orders_confirmed:
                    sleep(0.5)

                if in_id in self.inIds_to_orders_confirmed:
                    # get order msg on the book
                    order = self.inIds_to_orders_confirmed[in_id]
                    order['orderNo'] = self.inIds_to_exIds[in_id]

                    self.cancel_order(order)
                    self.logger.info(f"Cancelled order: \n"
                                     f"\t {order['symb']}: "
                                     f"{order['orderNo']} | "
                                     f"{order['side']} | "
                                     f"{order['origQty']} | "
                                     f"{order['remainingQty']} | "
                                     f"{order['price']}")

                    # qty to be filled in next round
                    qty += order['remainingQty']

                    # increment pv by filled qty
                    pv += order['price'] * (order['origQty'] - order['remainingQty'])

                # increment pv by fully filled amount
                else:
                    self.logger.info(f"Fully filled aggressive order: \n"
                                     f"\t {order['symb']}: "
                                     f"{order['orderNo']} | "
                                     f"{order['side']} | "
                                     f"{order['remainingQty']} | "
                                     f"{order['price']}")

                    pv += order['price'] * order['origQty']

        # avg execution price
        # is it possible to have qty > 0 still?
        cost_qty = pv / (qty_target - qty) - benchmark_price
        if action == 'sell':
            cost_qty *= -1

        logging.info(f'\n\t Aggressive order: {action} {qty_target-qty} {sym} given {min(time.time() - t_start, exec_t)} seconds: \n'
                     f'\t Transaction cost: {cost_qty} per share\n'
                     f'\t Benchmark price {benchmark_price}\n'
                     f'\t Benchmark VWAP: {benchmark_vwap}')
        if log:
            self.save_record('AggressiveNoSlice', sym, action, qty_target-qty, 1, min(time.time() - t_start, exec_t),
                             cost_qty, benchmark_price, benchmark_vwap)

        return pv, qty

    def twap_orders(self, qty, action, n_slices, exec_t=3.0):
        """
        send evenly allocated orders within fixed sub periods, with passive orders followed by aggressive orders
        :param qty: total target qty
        :param action: 'buy' or 'sell'
        :param exec_t: x seconds
        :param n_slices: # of slices
        :return: transaction cost per share = vwap (executed) - benchmark price
        """

        sym = self.securities[0]

        book_side = 'Bid' if action == 'buy' else 'Ask'
        side = 'B' if action == 'buy' else 'S'

        # benchmark price
        benchmark_price = self.mid_market[sym]
        benchmark_vwap = self.vwap[sym]

        # target qty
        qty_target = qty

        # pv = execution price * volume
        pv = 0

        # print(self.market_dict[sym])

        qty_slice = 0
        for i in range(n_slices):

            p = self.market_dict[sym]['L1'][book_side + 'Price']
            q = int(qty_target / n_slices) + qty_slice  # qty_slice = possible unfilled size in the previous slice

            order = {'symb': sym,
                     'price': p,
                     'origQty': q,
                     'status': "A",
                     'remainingQty': q,
                     'action': "A",
                     'side': side,
                     'FOK': 0,
                     'AON': 0,
                     'strategy': self.strategy,
                     'orderNo': self.internalID
                     }

            self.send_order(order)
            logging.info(f"Slice {i+1} - Limit order sent: \n"
                         f"\t {order['symb']}: "
                         f"{order['orderNo']} | "
                         f"{order['side']} | "
                         f"{order['remainingQty']} | "
                         f"{order['price']}")

            self.internalID += 1

            logging.info(f'Giving {exec_t} seconds for limit orders to be filled...')
            sleep(exec_t)

            # print(self.market_dict[sym])

            # make sure all orders are acked on matching enginee
            in_id = order["orderNo"]

            while in_id in self.inIds_to_orders_sent:
                sleep(0.001)
                # print(f'waiting for pending orders...')

            # cancel only if the order is not fully filled
            qty_slice = 0
            if in_id in self.inIds_to_orders_confirmed:
                # get order msg on the book
                order = self.inIds_to_orders_confirmed[in_id]
                order['orderNo'] = self.inIds_to_exIds[in_id]

                self.cancel_order(order)
                self.logger.info(f"Cancelled limit order {order['remainingQty']} out of {order['origQty']}: \n"
                                 f"\t {order['symb']}: "
                                 f"{order['orderNo']} | "
                                 f"{order['side']} | "
                                 f"{order['remainingQty']} | "
                                 f"{order['price']}")

                # qty to be filled aggressively
                qty_slice += order['remainingQty']

                # increment pv by fully filled amount
                pv += order['price'] * (order['origQty'] - order['remainingQty'])

                pv_slice, qty_slice = self.aggressive_orders(qty_slice, action)
                pv += pv_slice

            # increment pv by fully filled amount
            else:
                self.logger.info(f"Fully filled limit order: \n"
                                 f"\t {order['symb']}: "
                                 f"{order['orderNo']} | "
                                 f"{order['side']} | "
                                 f"{order['remainingQty']} | "
                                 f"{order['price']}")

                pv += order['price'] * order['origQty']

        # avg execution price
        cost_qty = pv / (qty_target - qty_slice) - benchmark_price
        if action == 'sell':
            cost_qty *= -1

        logging.info(f'\n\t Slicing order: {action} {qty_target-qty_slice} {sym}\n'
                     f'\t Given {n_slices} slices per {exec_t} seconds: \n'
                     f'\t Transaction cost: {cost_qty} per share\n'
                     f'\t Benchmark price: {benchmark_price}\n'
                     f'\t Benchmark VWAP: {benchmark_vwap}')

        self.save_record('TWAP', sym, action, qty, n_slices, exec_t*n_slices,
                         cost_qty, benchmark_price, benchmark_vwap)

    def vwap_orders(self):
        # need to know the market volume, either from yesterday's volume or some forecast
        # need to know the timestamp when placing order to lookup the period's market volume
        pass

    def pov_orders(self, qty, action, p_rate=0.5, sub_window=3.0):
        """
        send orders whose size is fixed percent of market volume
        assuming the volume within [t, t+dt] = volume within [t-dt, t]
        :param p_rate: fixed percent
        :param sub_window: the sub window to determine order size and place slices of orders
        """

        sym = self.securities[0]

        book_side = 'Bid' if action == 'buy' else 'Ask'
        side = 'B' if action == 'buy' else 'S'

        # benchmark price
        benchmark_price = self.mid_market[sym]
        benchmark_vwap = self.vwap[sym]

        # target qty
        qty_target = qty

        # pv = execution price * volume
        pv = 0

        # print(self.market_dict[sym])
        volume_s = self.traded_volume[sym]
        while self.traded_volume[sym] == volume_s:
            sleep(sub_window)
        volume_e = self.traded_volume[sym]

        time_s = time.time()

        qty_slice = 0
        i_slice = 1
        while qty_target > 0:

            p = self.market_dict[sym]['L1'][book_side + 'Price']

            # min qty = 0.1*qty
            q = int(min(max((volume_e - volume_s) * p_rate, 0.1*qty), qty_target))

            order = {'symb': sym,
                     'price': p,
                     'origQty': q,
                     'status': "A",
                     'remainingQty': q,
                     'action': "A",
                     'side': side,
                     'FOK': 0,
                     'AON': 0,
                     'strategy': self.strategy,
                     'orderNo': self.internalID
                     }

            self.send_order(order)
            logging.info(f"Slice {i_slice} - Passive order sent: \n"
                         f"\t {order['symb']}: "
                         f"{order['orderNo']} | "
                         f"{order['side']} | "
                         f"{order['remainingQty']} | "
                         f"{order['price']}")

            self.internalID += 1

            logging.info(f'Giving {sub_window} seconds for passive orders to be filled...')
            volume_s = self.traded_volume[sym]
            sleep(sub_window)

            # print(self.market_dict[sym])

            # make sure all orders are acked on matching engine
            in_id = order["orderNo"]

            while in_id in self.inIds_to_orders_sent:
                sleep(0.001)
                # print(self.inIds_to_orders_sent)
                # print(self.inIds_to_orders_confirmed)
                # print(f'waiting for pending orders...')

            # cancel only if the order is not fully filled
            in_id = order["orderNo"]
            qty_slice = 0
            if in_id in self.inIds_to_orders_confirmed:
                # get order msg on the book
                order = self.inIds_to_orders_confirmed[in_id]
                order['orderNo'] = self.inIds_to_exIds[in_id]

                self.cancel_order(order)
                self.logger.info(f"Cancelled limit order {order['remainingQty']} out of {order['origQty']}: \n"
                                 f"\t {order['symb']}: "
                                 f"{order['orderNo']} | "
                                 f"{order['side']} | "
                                 f"{order['remainingQty']} | "
                                 f"{order['price']}")

                # qty to be filled aggressively
                qty_slice += order['remainingQty']

                # increment pv by fully filled amount
                pv += order['price'] * (order['origQty'] - order['remainingQty'])

                pv_slice, qty_slice = self.aggressive_orders(qty_slice, action)
                pv += pv_slice

            # increment pv by fully filled amount
            else:
                self.logger.info(f"Fully filled limit order: \n"
                                 f"\t {order['symb']}: "
                                 f"{order['orderNo']} | "
                                 f"{order['side']} | "
                                 f"{order['remainingQty']} | "
                                 f"{order['price']}")

                pv += order['price'] * order['origQty']

            volume_e = self.traded_volume[sym]
            qty_target -= q - qty_slice
            i_slice += 1

        time_e = time.time()

        # avg execution price
        cost_qty = pv / qty - benchmark_price
        if action == 'sell':
            cost_qty *= -1

        logging.info(f'\n\t Slicing order: {action} {qty} {sym}\n'
                     f'\t Given {time_e-time_s} seconds: \n'
                     f'\t Transaction cost: {cost_qty} per share\n'
                     f'\t Benchmark price: {benchmark_price}\n'
                     f'\t Benchmark VWAP: {benchmark_vwap}')

        self.save_record('POV', sym, action, qty, i_slice-1, sub_window * (i_slice-1),
                         cost_qty, benchmark_price, benchmark_vwap)

    def save_record(self, exec_algo, sym, action, qty, slices, time, tc, bp, vwap):
        # save record into kdb
        record = {'AgentID': self.bot_id,
                  'Symb': sym,
                  'ExecAlgo': exec_algo,
                  'Date': datetime.datetime.now(),
                  'Action': action,
                  'ExecQty': qty,
                  'ExecSlices': slices,
                  'ExecTime(secs)': time,
                  'TransactionCost': tc,
                  'BenchmarkPrice': bp,
                  'BenchmarkVWAP': vwap
                }
        record = pd.DataFrame(record, index=[0])
        self.store('{`ExecutionAgents upsert x}', record)

if __name__ == "__main__":
    # market_event_securities = ["GEH0:MBO","GEM2:MBO","GEU0:MBO"]
    market_event_securities = ["ZBH0:MBO"]
    market_event_queue = ["L1", "L2","L3","L4","L5"]
    securities = market_event_securities

    host = "localhost"
    strategy = "Execution"
    bot_id = 'ExecutionAgent'
    starting_money = 1000000000.0

    exec_bot = ExecutionBot(strategy, starting_money, market_event_securities, market_event_queue, securities,
                           host, bot_id)

    for _ in range(10):
        exec_bot.aggressive_orders(500, 'sell', 5, log=True)
        exec_bot.twap_orders(500, 'buy', 2)
        exec_bot.pov_orders(500, 'sell')