#!/usr/bin/env python3
import psutil
import os

def print_logo():
    print(' _________  ____  _  __    _______   ____')
    print('/_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/')
    print(' / / / , _/ /_/ /    /___/ /__/ /___/ /  ')
    print('/_/ /_/|_|\____/_/|_/    \___/____/___/  ')
    print('-----------------------------------------')

# def print_logo_bg():
#     print('  _____   ____     ___    _   _            ____   _       ___ ')
#     print(' |_   _| |  _ \   / _ \  | \ | |          / ___| | |     |_ _|')
#     print('   | |   | |_) | | | | | |  \| |  _____  | |     | |      | | ')
#     print('   | |   |  _ <  | |_| | | |\  | |_____| | |___  | |___   | | ')
#     print('   |_|   |_| \_\  \___/  |_| \_|          \____| |_____| |___|')

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
