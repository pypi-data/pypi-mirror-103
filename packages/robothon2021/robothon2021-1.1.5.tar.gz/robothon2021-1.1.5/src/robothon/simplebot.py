import sys
sys.path.append('../')

import uuid
import random
import logging
format = "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s() line: %(lineno)d: %(message)s"
logging.basicConfig(format=format)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

from Management import Management


class SimpleBot(Management):

    def __init__(self, strategy, starting_money,
                 market_event_securities, market_event_queue, securities,
                 host=None, bot_id=None):

        super(SimpleBot, self).__init__(strategy, starting_money,
                                        market_event_securities, market_event_queue, securities,
                                        host, bot_id)

        # # Subscription to order book in order to passively send orders
        # self.kickoff()

        # actively send orders
        self.start()

    def _model_reaction_to_level(self, tob):
        qty = 100
        side = 'B'

        # for testing, to reduce the frequency of sending order
        #if  len(self.mgr.inIds_to_orders_sent) != 0:
        #    return
        
        if True:    # self.mgr.bid_trend[self.sec2]["L1"] == 1:
            # log.debug(self.mgr.mid_market)

            if self.mid_market[tob["symb"]] is not None:
                order = {'symb': tob["symb"],
                        'price': self.mid_market[tob["symb"]],
                        'origQty': qty,
                        'status': "A",
                        'remainingQty': qty,
                        'action': "A",
                        'side': side,
                        'FOK': 0,
                        'AON': 0,
                        'strategy': self.strategy,
                        }
                log.info("\nTry to Send Order:")
                order['orderNo'] = self.internalID
                self.internalID += 1
                log.info(order)
                self.send_order(order)


if __name__ == "__main__":
    #market_event_securities = ["GEH0:MBO","GEM2:MBO","GEU0:MBO"]
    market_event_securities = ["GEH0:MBO", "ZNH0:MBO", "ZBH0:MBO", "ZFH0:MBO", "ZTH0:MBO", "UBH0:MBO"]
    market_event_queue = ["L1", "L2", "L3"]
    securities = market_event_securities

    #host = "172.29.208.37"
    host = "localhost"
    strategy = "A1067"
    bot_id = 'TestBot'
    starting_money = 1000000000.0

    simple_bot = SimpleBot(strategy, starting_money, market_event_securities, market_event_queue, securities,
                           host, 'TestBot1')
    simple_bot = SimpleBot(strategy, starting_money, market_event_securities, market_event_queue, securities,
                           host, 'TestBot2')
    simple_bot = SimpleBot(strategy, starting_money, market_event_securities, market_event_queue, securities,
                           host, 'TestBot3')
    simple_bot = SimpleBot(strategy, starting_money, market_event_securities, market_event_queue, securities,
                           host, 'TestBot4')
    simple_bot = SimpleBot(strategy, starting_money, market_event_securities, market_event_queue, securities,
                           host, 'TestBot5')
