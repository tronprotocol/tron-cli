# import os
import json

# from init import Init
from utils import Phrase, success_msg, warnning_msg, msg
from json_store import raw_config

class Config(object):
    """handler for setup config files"""
    def __init__(self):
        self.config = None

    @classmethod
    def init(cls):
        """
        Load raw json config
        load - change - dump
        make path and dirs constant
        """
        # init = Init()
        # cls.fullnode_path = init.root_path + init.nodes_dir + init.fullnode_dir + '/raw.json'
        # print(cls.fullnode_path)
        # print(raw_config_json)
        phrase = Phrase()
        cls.config = raw_config
        # json_props = phrase.load_json_file(cls.fullnode_path)
        # print(cls.config[' net'])
        success_msg('config initialized')
        # properties_str = phrase.json2properties_file('/Users/weiyu/Code/TRON/tron-cli/tron-cli/raw.json', 
        #     '/Users/weiyu/Code/TRON/tron-cli/temp/tron_nodes/fullnode/full.conf')



