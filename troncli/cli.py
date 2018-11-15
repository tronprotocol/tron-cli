#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /  
# /_/ /_/|_|\____/_/|_/    \___/____/___/
import os
import asyncio
import cbox

from troncli import utils, h_init, h_config, h_worker


@cbox.cmd
def init(version: str):
    """Init dirs and fetch code.
    >> 
    Settings: 
        --version
    >>
    """
    # Example:
    #     tron-cli init --version latest

    init_handler = h_init.Init()
    utils.progress_msg('Creating folders')
    init_handler.create_dirs()
    utils.progress_msg('Downloading release builds')
    asyncio.run(init_handler.fetch_jars(version))
    asyncio.run(init_handler.move_jars())


@cbox.cmd
def config(nettype: str, fullhttpport: int, solhttpport: int, fullgrpcport: int, solgrpcport: int):
    """Create customize config files.
    >> 
    Settings: 
        --nettype
        --fullhttpport
        --solhttpport
        --fullgrpcport
        --solgrpcport
    """
    # >>
    # Example:
    #     tron-cli config --nettype 'private' --fullhttpport 8500 --solhttpport 8600 --fullgrpcport 50051 --solgrpcport 5001

    config_handler = h_config.Config()
    utils.progress_msg('Setting up config files')
    asyncio.run(config_handler.init())
    asyncio.run(config_handler.set_net_type(nettype))
    asyncio.run(config_handler.set_http_port(fullhttpport, 'full'))
    asyncio.run(config_handler.set_http_port(solhttpport, 'sol'))
    asyncio.run(config_handler.set_grpc_port(fullgrpcport, 'full'))
    asyncio.run(config_handler.set_grpc_port(solgrpcport, 'sol'))
    asyncio.run(config_handler.export())


@cbox.cmd
def run(nodetype: str):
    """Run node.
    >> 
    Settings: 
        --nodetype
    """
    utils.progress_msg('Starting node(s)')
    worker = h_worker.Worker()
    asyncio.run(worker.run(nodetype))


@cbox.cmd
def stop(pid: str):
    """Stop node.
    >> 
    Settings: 
        --pid
    """
    worker = h_worker.Worker()
    utils.progress_msg('Shutting down node(s)')
    asyncio.run(worker.stop(pid))


@cbox.cmd
def quick():
    """Quick start. (run a full private node by one command)
    >>
    Example:
        tron-cli quick
    """
    utils.logo()
    init('lastest')
    config('private', 8500, 8600, 50051, 50001)
    run('full')
    

def main():
    cbox.main([init, config, run, stop, quick])
    

if __name__ == '__main__':
    main()

