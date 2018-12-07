#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /
# /_/ /_/|_|\____/_/|_/    \___/____/___/

import asyncio
import cbox

from troncli import utils, h_init, h_config, h_worker, h_status


@cbox.cmd
def init(version: str = 'lastest'):
    """Init dirs and fetch code.

    :param version: specify java-tron version
    """

    init_handler = h_init.Init()
    utils.progress_msg('Creating folders')
    init_handler.create_dirs()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_handler.fetch_jars(version))
    loop.run_until_complete(init_handler.move_jars())


@cbox.cmd
def config(nettype: str = 'private',
           fullhttpport: int = 8500,
           solhttpport: int = 8600,
           fullrpcport: int = 50051,
           solrpcport: int = 50001,
           enablememdb: str = 'True'):
    """Create customize config files.

    :param nettype: specify net type [main, private]
    :param fullhttpport: specify full http port
    :param solhttpport: specify solidity http port
    :param fullrpcport: specify full rpc port
    :param solrpcport: specify solidity rpc port
    """

    config_handler = h_config.Config()
    utils.progress_msg('Setting up config files')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(config_handler.init())
    loop.run_until_complete(config_handler.set_net_type(nettype))
    loop.run_until_complete(config_handler.set_http_port(fullhttpport, 'full'))
    loop.run_until_complete(config_handler.set_http_port(solhttpport, 'sol'))
    loop.run_until_complete(config_handler.set_rpc_port(fullrpcport, 'full'))
    loop.run_until_complete(config_handler.set_rpc_port(solrpcport, 'sol'))
    loop.run_until_complete(config_handler.set_db_version(enablememdb))
    loop.run_until_complete(config_handler.export())


@cbox.cmd
def run(nodetype: str = 'full'):
    """Run node.
    
    :param nodetype: specify node type [full, sol]
    """
    utils.progress_msg('Starting node(s)')
    worker = h_worker.Worker()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.run(nodetype))
    loop.close()


@cbox.cmd
def stop(pid: str):
    """Stop node.
    
    :param pid: stop node by given pid 
    """
    worker = h_worker.Worker()
    utils.progress_msg('Shutting down node(s)')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.stop(pid))
    loop.close()


@cbox.cmd
def status(node: str = 'all'):
    """Monitor nodes status.
    
    :param node: check specific node detail by pid
    """
    status_handler = h_status.Status()
    if node == 'all':
        status_handler.overall()
    else:
        status_handler.ps(int(node))


@cbox.cmd
def quick():
    """Quick start. (run a full private node by one command)
    """
    utils.logo()
    init()
    config()
    run()
    status()


def main():
    cbox.main([init, config, run, stop, status, quick])


if __name__ == '__main__':
    main()
