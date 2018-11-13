#!/usr/bin/env python3
import psutil
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import re

"""
Printing Messages
"""
def logo():
    print(' _________  ____  _  __    _______   ____')
    print('/_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/')
    print(' / / / , _/ /_/ /    /___/ /__/ /___/ /  ')
    print('/_/ /_/|_|\____/_/|_/    \___/____/___/  ')

def progress_msg(content):
    print('[ TRON-CLI ]: ' + content + '...')

def success_msg(content):
    print('✓ : ' + content)

def warnning_msg(content):
    print('⚠ : ' + content)

def error_msg(content):
    print('✖ : ' + content)

def msg(content):
    print('    ' + content)

"""
Download
"""
async def download(file_name, url_string):
    with open(file_name, 'wb') as f:
        # remove warnings
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        resp = requests.get(url_string + '/' + file_name, verify=False)
        f.write(resp.content)

def test():
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    cwd = os.getcwd()
    print('cwd: ', cwd)

    virt = psutil.virtual_memory()
    swap = psutil.swap_memory()
    templ = "%-7s %10s %10s %10s %10s %10s %10s"
    print(templ % ('', 'total', 'used', 'free', 'shared', 'buffers', 'cache'))
    print(templ % (
        'Mem:',
        int(virt.total / 1024),
        int(virt.used / 1024),
        int(virt.free / 1024),
        int(getattr(virt, 'shared', 0) / 1024),
        int(getattr(virt, 'buffers', 0) / 1024),
        int(getattr(virt, 'cached', 0) / 1024)))
    print(templ % (
        'Swap:', int(swap.total / 1024),
        int(swap.used / 1024),
        int(swap.free / 1024),
        '',
        '',
        ''))

class Phrase(object):
    def load_json_file(self, json_file_path):
        f = open(json_file_path)
        _json_props = json.load(f)
        f.close()
        return _json_props
        
        
    def store_json2properties_to_file(self, json_props, target_file_path):
        """
        convert json to properties and store in target file
        """
        _properties = self.json2properties(json_props)
        _properties_str_formatted = self.properties2str(_properties)
        f = open(target_file_path, 'w')
        f.write(_properties_str_formatted)
        f.close()

    def properties2str(self, properties_props):
        """
        convert properties to string, and change format
        """
        _formatted_str = str(properties_props)
        _formatted_str = re.sub("}, '", "},\n\n'", _formatted_str)
        _formatted_str = re.sub("':", ":", _formatted_str)
        _formatted_str = re.sub("' ", "", _formatted_str)
        _formatted_str = re.sub("'", "\"", _formatted_str)
        return _formatted_str


    def json2properties(self, json_props):
        """
        Credit: this function is based on the phrase code in the project:
            echinopsii/net.echinopsii.ariane.community.cli.python3.
        """
        properties = {}
        if isinstance(json_props, list):
            for prop in json_props:
                if isinstance(prop['propertyValue'], list):
                    properties[prop['propertyName']] = prop['propertyValue'][1]

                elif isinstance(prop['propertyValue'], dict):
                    map_property = {}
                    for prop_key, prop_value in prop['propertyValue'].items():
                        if prop_value.__len__() > 1:
                            map_property[prop_key] = prop_value[1]
                        else:
                            print("json2properties - " + prop_key +
                                        " will be ignored as its definition is incomplete...")
                    properties[prop['propertyName']] = map_property

                elif prop['propertyType'] == 'array':
                    j_data = json.loads(prop['propertyValue'])
                    if j_data.__len__() > 1:
                        if j_data[0] == "map":
                            t_data = []
                            for amap in j_data[1]:
                                t_data.append(DriverTools.json_map2properties(amap))
                            properties[prop['propertyName']] = t_data
                        elif j_data[0] == "array":
                            t_data = []
                            for ar in j_data[1]:
                                t_data.append(DriverTools.json_array2properties(ar))
                            properties[prop['propertyName']] = t_data
                        else:
                            properties[prop['propertyName']] = j_data[1]
                    else:
                        print("json2properties - " + prop['propertyName'] +
                                    " will be ignored as its definition is incomplete...")

                elif prop['propertyType'] == 'map':
                    j_data = json.loads(prop['propertyValue'])
                    map_property = DriverTools.json_map2properties(j_data)
                    properties[prop['propertyName']] = map_property

                else:
                    properties[prop['propertyName']] = prop['propertyValue']
        else:
            properties = json_props
        return properties


