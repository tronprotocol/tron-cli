# import os
import json

# from init import Init
from utils import Phrase, success_msg, warnning_msg, msg
from json_store import raw_config
from constants import *

class Config(object):
    """handler for setup config files"""
    def __init__(self, root_path):
        self.root_path = root_path
        self.config = None

    @classmethod
    def init(cls):
        """
        Load raw json config
        """
        phrase = Phrase()
        cls.config = raw_config
        success_msg('config initialized')

    def export(self):
        """
        Export properties config file
        """
        phrase = Phrase()
        print('self.root_path ', self.root_path)
        _target_file_path = self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_CONFIG
        phrase.store_json2properties_to_file(self.config, _target_file_path)
        success_msg('config file exported to: ' + _target_file_path)


