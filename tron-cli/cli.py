#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /  
# /_/ /_/|_|\____/_/|_/    \___/____/___/
import os
import asyncio
import cbox
# from subprocess import call
import subprocess as sub

from utils import logo, progress_msg
from init import Init
from config import Config
from constants import *

ROOT_PATH = ''


@cbox.cmd
def init(version: str):
    """init dirs and fetch code.
    """
    init_handler = Init(ROOT_PATH)
    progress_msg('Creating folders')
    init_handler.create_dirs()
    progress_msg('Downloading release builds')
    asyncio.run(init_handler.fetch_jars(version))
    asyncio.run(init_handler.move_jars())


@cbox.cmd
def config():
    """customize config files.
    """
    config_handler = Config(ROOT_PATH)
    progress_msg('Setting up config files')
    asyncio.run(config_handler.init())
    asyncio.run(config_handler.export())


@cbox.cmd
def run():
    """run nodes.
    """
    progress_msg('Starting node(s)')
    pro = sub.Popen(["java", "-jar", ROOT_PATH + NODES_DIR + FULL_NODE_DIR + FULL_NODE_JAR, 
            "-c", ROOT_PATH + NODES_DIR + FULL_NODE_DIR + FULL_CONFIG, 
            "--witness"])
    # print('os.getpgid(pro.pid): ', os.getpgid(pro.pid))


@cbox.cmd
def quick():
    logo()
    init('lastest')
    config()
    run()


if __name__ == '__main__':
    ROOT_PATH = os.getcwd()
    cbox.main([init, config, run, quick])

