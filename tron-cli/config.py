# import os
import javaproperties

class Config(object):
    """handler for init dirs and fetch code"""
    def __init__(self):
        self.fullnode_dir = '/tron_nodes'
        self.config = None

    def init(self):
        # self.config = configparser.ConfigParser()
        # self.config['net'] = {'type' : 'mainnet'}
        # with open('main.conf', 'w') as configfile:
        #     self.config.write(configfile)

        # p = Properties()
        # p["foobar"] = "A very important message from our sponsors: Python is great!"

        # with open("foobar.properties", "wb") as f:
        #     p.store(f, encoding="utf-8")
        # sub_obj = {'type' : 'mainnet', }
        properties_obj = {'net.type': 'testnet', }
        self.generate_conf_properties('/Users/weiyu/Code/TRON/tron-cli/temp/tron_nodes/fullnode/full.conf', 
            properties_obj)

    def generate_conf_properties(self, filename, modified_properties):
        with open('/Users/weiyu/Code/TRON/tron-cli/tron-cli/raw.conf', 'r') as fp:
            properties = javaproperties.load(fp)
            print(properties)

        with open(filename, 'w') as fp:
            properties.update(modified_properties)
            print(properties)
            javaproperties.dump(properties, fp)


