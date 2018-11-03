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
        """
        phrase = Phrase()
        cls.config = raw_config
        success_msg('config initialized')

    @classmethod
    def export(cls, target_file_path):
        """
        Export properties config file
        """
        phrase = Phrase()
        phrase.store_json2properties_to_file(cls.config, target_file_path)
        success_msg('config file exported to: ' + target_file_path)


