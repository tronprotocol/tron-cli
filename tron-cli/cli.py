#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /  
# /_/ /_/|_|\____/_/|_/    \___/____/___/
from utils import print_logo

import cbox


@cbox.cmd
def init():
    """init dirs and fetch code.
    """
    print_logo()


@cbox.cmd
def config():
    """customize config files.
    """
    print_logo()


@cbox.cmd
def run():
    """run nodes.
    """
    print_logo()


@cbox.cmd
def quick():
    print('quick start')


if __name__ == '__main__':
    cbox.main([init, config, run, quick])

