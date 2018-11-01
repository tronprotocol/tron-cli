#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /  
# /_/ /_/|_|\____/_/|_/    \___/____/___/
import asyncio
import cbox

from utils import print_logo
from init import Init


@cbox.cmd
def init(version: str):
    """init dirs and fetch code.
    """
    InitHandler = Init()
    InitHandler.create_dirs()
    asyncio.run(InitHandler.fetch_jars('3.1.3'))
    asyncio.run(InitHandler.move_jars())


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
    print_logo()
    print('quick start')


if __name__ == '__main__':
    cbox.main([init, config, run, quick])

