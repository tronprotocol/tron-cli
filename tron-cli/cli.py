#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /  
# /_/ /_/|_|\____/_/|_/    \___/____/___/
import asyncio
import cbox

from utils import logo, progress_msg
from init import Init
from config import Config


@cbox.cmd
def init(version: str):
    """init dirs and fetch code.
    """
    init_handler = Init()
    progress_msg('Creating folders')
    init_handler.create_dirs()
    progress_msg('Downloading release builds')
    asyncio.run(init_handler.fetch_jars('3.1.3'))
    asyncio.run(init_handler.move_jars())


@cbox.cmd
def config():
    """customize config files.
    """
    config_handler = Config()
    progress_msg('Setting up config files')
    config_handler.init()


@cbox.cmd
def run():
    """run nodes.
    """
    logo()


@cbox.cmd
def quick():
    logo()
    init('lastest')


if __name__ == '__main__':
    cbox.main([init, config, run, quick])

