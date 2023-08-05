from pkg_resources import Requirement, resource_filename
import os
import shutil
import site

def main():
    CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'robothon')

    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    
    files = ['config.py', 'executionbot.py', 'simplebot.py']
    for file_name in files:
        if os.path.isfile(file_name):
            shutil.copy(file_name, CONFIG_PATH)
