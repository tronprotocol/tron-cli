#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /
# /_/ /_/|_|\____/_/|_/    \___/____/___/

import asyncio
import cbox

from troncli import utils, h_init, h_config, h_worker, h_status, __version__


@cbox.cmd
def init(version: str = 'lastest',
         reset: str = 'False'):
    """Init dirs and fetch code.

    :param version: specify java-tron version
    """

    init_handler = h_init.Init()
    utils.progress_msg('Creating folders')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_handler.env_check())
    loop.run_until_complete(init_handler.create_dirs(reset))
    loop.run_until_complete(init_handler.fetch_jars(version))
    loop.run_until_complete(init_handler.move_jars())
    loop.run_until_complete(init_handler.fetch_code())


@cbox.cmd
def config(nettype: str = 'private',
           fullhttpport: int = 8500,
           solhttpport: int = 8600,
           eventhttpport: int = 8400,
           fullrpcport: int = 58500,
           solrpcport: int = 58600,
           eventrpcport: int = 58400,
           enablememdb: str = 'True',
           dbsyncmode: str = 'async',
           saveintertx: str = 'False',
           savehistorytx: str = 'False',
           gridport: int = 18891,
           dbname: str = 'Null',
           dbusername: str = 'Null',
           dbpassword: str = 'Null'
           ):
    """Create customize config files.

    :param nettype: specify net type [main, private]
    :param fullhttpport: specify full node http port
    :param solhttpport: specify solidity node http port
    :param eventhttpport: specify event node http port
    :param fullrpcport: specify full node rpc port
    :param solrpcport: specify solidity node rpc port
    :param eventrpcport: specify event node rpc port
    :param enablememdb: enable/disable in memory db
    :param gridport: specify grid api port
    :param dbsyncmode: specify either db async or sync mode
    :param saveintertx: enable/disable save internal transcation
    :param savehistorytx: enable/disable save history transcation
    :param dbname: specify db name
    :param dbusername: specify db user name
    :param dbpassword: specify db password name
    """

    config_handler = h_config.Config()
    node_list = utils.Node()
    utils.progress_msg('Setting up config files')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(config_handler.init())
    loop.run_until_complete(config_handler.set_net_type(nettype))
    loop.run_until_complete(config_handler.set_http_port(fullhttpport, 'full', nettype))
    loop.run_until_complete(config_handler.set_http_port(solhttpport, 'sol', nettype))
    loop.run_until_complete(config_handler.set_http_port(eventhttpport, 'event', nettype))
    loop.run_until_complete(config_handler.set_rpc_port(fullrpcport, 'full'))
    loop.run_until_complete(config_handler.set_rpc_port(solrpcport, 'sol'))
    loop.run_until_complete(config_handler.set_rpc_port(eventrpcport, 'event'))
    loop.run_until_complete(config_handler.set_db_version(enablememdb))
    loop.run_until_complete(config_handler.set_db_sync_mode(dbsyncmode))
    loop.run_until_complete(config_handler.enable_save_inter_tx(saveintertx))
    loop.run_until_complete(config_handler.enable_save_history_tx(savehistorytx))
    loop.run_until_complete(config_handler.export())
    loop.run_until_complete(config_handler.store_db_settings(dbname, dbusername, dbpassword, gridport))
    loop.run_until_complete(node_list.update_config(nettype, fullhttpport, solhttpport,
                                                             eventhttpport, fullrpcport, solrpcport, eventrpcport,
                                                             enablememdb, dbsyncmode, saveintertx, savehistorytx, 
                                                             gridport, dbname, dbusername, dbpassword))


@cbox.cmd
def run(nodetype: str = 'full'):
    """Run node.
    
    :param nodetype: specify node type [full, sol, event]
    """
    worker = h_worker.Worker()
    utils.progress_msg('Starting node(s)')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.run(nodetype))
    loop.close()


@cbox.cmd
def stop(node: str = 'all'):
    """Stop node.
    
    :param node: stop node by given node id or all
    """
    worker = h_worker.Worker()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.stop(node))
    loop.close()


@cbox.cmd
def status(node: str = 'all'):
    """Monitor nodes status.
    
    :param node: check specific node detail by node id
    """
    status_handler = h_status.Status()
    if node == 'all':
        status_handler.overall()
    else:
        status_handler.ps(int(node))


@cbox.cmd
def quick(reset: str = 'False'):
    """Quick start. (run a full private node by one command)
    """
    utils.logo_shadow()
    init('lastest', reset)
    config()
    run()
    status()

@cbox.cmd
def version():
    """Check installed troncli version.
    """
    utils.msg(str(__version__))


def main():
    cbox.main([init, config, run, stop, status, quick, version])


if __name__ == '__main__':
    main()
