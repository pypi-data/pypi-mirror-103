from pkg_resources import Requirement, resource_filename
import os
import shutil
import site

def main():

    CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'robothon')

    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
        
    cur_path = os.path.join(site.USER_BASE, 'lib/python3.7/site-packages/robothon')
    
    files = ['config.py', 'executionbot.py', 'simplebot.py']
    for file_name in files:
        full_file_path = os.path.join(cur_path, file_name)
        if os.path.isfile(full_file_path):
            shutil.copy(full_file_path, CONFIG_PATH)
