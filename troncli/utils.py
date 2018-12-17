#!/usr/bin/env python3
import os
import requests
import json
import sys
import psutil
import subprocess
import re
from colorama import Fore, Style
from tqdm import tqdm

import urllib3
from troncli.constants import *

"""
Printing Messages
"""


def logo():
    print(Fore.RED + ' _________  ____  _  __    _______   ____')
    print(Fore.RED + '/_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/')
    print(Fore.RED + ' / / / , _/ /_/ /    /___/ /__/ /___/ /  ')
    print(Fore.RED + '/_/ /_/|_|\____/_/|_/    \___/____/___/  ')


def progress_msg(content):
    print(Fore.CYAN + '[ TRON-CLI ]: ' + content + '...' + Fore.RESET)


def success_msg(content):
    print(Fore.GREEN + '✓ : ' + content + Fore.BLACK)


def warning_msg(content):
    print(Fore.YELLOW + '⚠ : ' + content)


def error_msg(content):
    print(Fore.RED + '✖ : ' + content)


def info_msg(content):
    print(Fore.MAGENTA + 'ⓘ: ' + content + Fore.RESET)


def status_msg(category, detail):
    if sys.stdout.isatty() and psutil.POSIX:
        fmt = '%-13s %s' % (Fore.BLUE + Style.BRIGHT + str(category),
                            Fore.RESET + Style.RESET_ALL + str(detail))
    else:
        fmt = '%-11s %s' % (category, detail)
    print(fmt)


def msg(content):
    print(Fore.RESET + '    ' + content + Fore.RESET)


def debug(content):
    print(Fore.YELLOW + Style.BRIGHT + 'DEBUG:  ' + content + Fore.RESET + Style.RESET_ALL)


"""
Node List
"""


class Node(object):
    def __init__(self):
        self.root_path = os.getcwd()
        # load or init node list file
        if os.path.isfile(self.root_path + '/' + RUNNING_NODE_LIST_FILE):
            phrase = Phrase()
            self.node_list = phrase.load_json_file(self.root_path + '/' + RUNNING_NODE_LIST_FILE)
        else:
            self.node_list = {'full': [], 'sol': [], 'event': [], 'grid': [],
                              'db': {'dbname': '', 'dbusername': '', 'dbpassword': ''}}

    async def get(self):
        return self.node_list

    async def update_running_node(self, node_type, pid, execution):
        """
        node_type: "full" / "sol"
        pid: int
        execution: "add" / "remove"
        """
        if execution == 'add':
            self.node_list[node_type].append(pid)
        elif execution == 'remove':
            if pid in self.node_list['full']:
                self.node_list['full'].remove(pid)
            elif pid in self.node_list['sol']:
                self.node_list['sol'].remove(pid)
            elif pid in self.node_list['event']:
                self.node_list['event'].remove(pid)
            elif pid in self.node_list['grid']:
                self.node_list['grid'].remove(pid)
            else:
                warning_msg('process id: ' + str(pid) + ' not in the running node list')
        else:
            error_msg('wrong execution key word: ' + str(execution))

        with open(self.root_path + '/' + RUNNING_NODE_LIST_FILE, 'w') as file:
             file.write(json.dumps(self.node_list))

    async def update_db_settings(self, dbname, dbusername, dbpassword):
        self.node_list['db']['dbname'] = dbname
        self.node_list['db']['dbusername'] = dbusername
        self.node_list['db']['dbpassword'] = dbpassword

        with open(self.root_path + '/' + RUNNING_NODE_LIST_FILE, 'w') as file:
             file.write(json.dumps(self.node_list))

    async def update_ports():
        pass

"""
Download
"""


async def download(file_name, url_string):
    with open(file_name, 'wb') as f:
        # remove ssl warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            resp = requests.get(url_string + '/' + file_name,
                                verify=False, stream=True)

        except OSError as err:
            # pbar.update(0)
            error_msg('OS Error -' + str(err))
            os.sys.exit()

        else:
            with tqdm(total=100) as pbar:
                total_length = resp.headers.get('content-length')
                if total_length is None:
                    pbar.update(100)
                    pbar.close()
                    f.write(resp.content)
                else:
                    _chunk_num = 10
                    _chunk_size = int(int(total_length) / _chunk_num) + 1
                    for data in resp.iter_content(chunk_size=_chunk_size):
                        f.write(data)
                        pbar.update(_chunk_num)
                    pbar.close()


async def git_clone(host, branch, tar_path):
    progress_msg('Git cloning ' + host + '-branch: ' + branch)
    cmd = 'git clone --single-branch -b ' + branch + ' ' + host
    cmd += ' ' + tar_path
    # _process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
    os.system(cmd)

async def gradlew_build(task):
    cmd = './gradlew build -x test'
    try:
        os.system(cmd)
    except OSError as err:
        error_msg('OS Error -' + str(err))
        os.sys.exit()
    else:
        success_msg(task + ' gradlew build finished')


"""
Phrase
"""


class Phrase(object):
    @staticmethod
    def convert_bytes(n):
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
        return "%sB" % n

    @staticmethod
    def load_json_file(json_file_path):
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

    def store_json2javabeanconfig_to_file(self, json_props, target_file_path):
        """
        convert json to properties and store in target file
        """
        _properties = self.json2properties(json_props)
        _properties_str_formatted = self.properties2str_bean(_properties)
        f = open(target_file_path, 'w')
        f.write(_properties_str_formatted)
        f.close()

    @staticmethod
    def properties2str(properties_props):
        """
        convert properties to string, and change format
        """
        _formatted_str = str(properties_props)
        _formatted_str = re.sub("}, '", "},\n\n'", _formatted_str)
        _formatted_str = re.sub("':", ":", _formatted_str)
        _formatted_str = re.sub("' ", "", _formatted_str)
        _formatted_str = re.sub("'", "\"", _formatted_str)
        return _formatted_str

    @staticmethod
    def properties2str_bean(properties_props):
        """
        convert properties to string, and change format
        """
        _formatted_str = str(properties_props)
        _formatted_str = re.sub("}, '", "},\n\n'", _formatted_str)
        _formatted_str = re.sub("':", ":", _formatted_str)
        _formatted_str = re.sub("' ", "", _formatted_str)
        _formatted_str = re.sub("'", "\"", _formatted_str)
        _formatted_str = re.sub(":", " =", _formatted_str)
        _formatted_str = re.sub(", ", "\r", _formatted_str)
        _formatted_str = re.sub("\"", "", _formatted_str)
        return _formatted_str[1:-1]

    @staticmethod
    def json2properties(json_props):
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
                            print('json2properties - ' + prop_key +
                                  ' will be ignored as its definition is incomplete...')
                    properties[prop['propertyName']] = map_property

                elif prop['propertyType'] == 'array':
                    j_data = json.loads(prop['propertyValue'])
                    if j_data.__len__() > 1:
                        if j_data[0] == 'map':
                            t_data = []
                            for amap in j_data[1]:
                                t_data.append(DriverTools.json_map2properties(amap))
                            properties[prop['propertyName']] = t_data
                        elif j_data[0] == 'array':
                            t_data = []
                            for ar in j_data[1]:
                                t_data.append(DriverTools.json_array2properties(ar))
                            properties[prop['propertyName']] = t_data
                        else:
                            properties[prop['propertyName']] = j_data[1]
                    else:
                        print('json2properties - ' + prop['propertyName'] +
                              ' will be ignored as its definition is incomplete...')

                elif prop['propertyType'] == 'map':
                    j_data = json.loads(prop['propertyValue'])
                    map_property = DriverTools.json_map2properties(j_data)
                    properties[prop['propertyName']] = map_property

                else:
                    properties[prop['propertyName']] = prop['propertyValue']
        else:
            properties = json_props
        return properties
