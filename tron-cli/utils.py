#!/usr/bin/env python3
import psutil
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def print_logo():
    print(' _________  ____  _  __    _______   ____')
    print('/_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/')
    print(' / / / , _/ /_/ /    /___/ /__/ /___/ /  ')
    print('/_/ /_/|_|\____/_/|_/    \___/____/___/  ')
    print('-----------------------------------------')

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
