# import os
import json
import copy

# from init import Init
from utils import Phrase, success_msg, warnning_msg, msg
from json_store import raw_config
from constants import *

class Config(object):
    """handler for setup config files"""
    def __init__(self, root_path):
        self.root_path = root_path
        self.full_config = None
        self.sol_config = None

    async def init(self):
        """
        Load raw json config
        """
        phrase = Phrase()
        self.full_config = copy.deepcopy(raw_config)
        self.sol_config = copy.deepcopy(raw_config)
        success_msg('config initialized')

    async def export(self):
        """
        Export properties config file
        """
        phrase = Phrase()
        _target_file_path_full = self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_CONFIG
        phrase.store_json2properties_to_file(self.full_config, _target_file_path_full)
        success_msg('fullnode config file exported to: ' + _target_file_path_full)

        _target_file_path_sol = self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOL_CONFIG
        phrase.store_json2properties_to_file(self.sol_config, _target_file_path_sol)
        success_msg('soliditynode config file exported to: ' + _target_file_path_sol)


    async def set_http_port(self, port_num, node_type):
        if node_type == 'full':
            self.full_config[' node'][' http'][' fullNodePort'] = port_num
        elif node_type == 'sol':
            self.sol_config[' node'][' http'][' solidityPort'] = port_num
        else:
            warnning_msg('wrong node_type')


