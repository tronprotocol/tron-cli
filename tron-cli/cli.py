#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /  
# /_/ /_/|_|\____/_/|_/    \___/____/___/
import asyncio
import cbox

from utils import logo, progress_msg
from init import Init


@cbox.cmd
def init(version: str):
    """init dirs and fetch code.
    """
    InitHandler = Init()
    progress_msg('Creating foldres')
    InitHandler.create_dirs()
    progress_msg('Download release builds')
    asyncio.run(InitHandler.fetch_jars('3.1.3'))
    asyncio.run(InitHandler.move_jars())


@cbox.cmd
def config():
    """customize config files.
    """
    logo()


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

