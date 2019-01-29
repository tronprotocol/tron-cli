#!/usr/bin/env python3
#  _________  ____  _  __    _______   ____
# /_  __/ _ \/ __ \/ |/ /___/ ___/ /  /  _/
#  / / / , _/ /_/ /    /___/ /__/ /___/ /
# /_/ /_/|_|\____/_/|_/    \___/____/___/

import asyncio
import cbox

from troncli import utils, h_init, h_config, h_worker, h_status, h_log, __version__, h_imode
from troncli.constants import *


@cbox.cmd
def init(version: str = 'latest',
         reset: str = 'False'):
    """Init dirs and fetch code.

    :param reset: reset all
    :param version: specify java-tron version
    """

    init_handler = h_init.Init()
    utils_handler = utils.Node()
    utils.progress_msg('Creating folders')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(utils_handler.update_init_done(False))
    loop.run_until_complete(utils_handler.update_config_done(False))
    loop.run_until_complete(init_handler.env_check())
    loop.run_until_complete(init_handler.create_dirs(reset))
    loop.run_until_complete(init_handler.fetch_jars(version))
    loop.run_until_complete(init_handler.fetch_code())
    # loop.run_until_complete(init_handler.build_eventnode_jar())
    # loop.run_until_complete(init_handler.build_gridapi_jar())
    loop.run_until_complete(init_handler.move_jars())
    loop.run_until_complete(utils_handler.update_init_done(True))


@cbox.cmd
def config(nettype: str = '',
           fullhttpport: int = 0,
           solhttpport: int = 0,
           eventhttpport: int = 0,
           fullrpcport: int = 0,
           solrpcport: int = 0,
           eventrpcport: int = 0,
           enablememdb: str = '',
           dbsyncmode: str = '',
           saveintertx: str = '',
           savehistorytx: str = '',
           gridport: int = 0,
           dbname: str = 'Null',
           dbusername: str = 'Null',
           dbpassword: str = 'Null',
           reset: str = 'False'
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
    :param reset: reset config to default settings
    """

    config_handler = h_config.Config()
    utils_handler = utils.Node()
    utils.progress_msg('Setting up config files')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(utils_handler.update_config_done(False))
    loop.run_until_complete(config_handler.init(reset))
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
    loop.run_until_complete(config_handler.store_db_settings(dbname, dbusername, dbpassword, gridport))
    loop.run_until_complete(config_handler.export())
    loop.run_until_complete(utils_handler.update_config_done(True))


@cbox.cmd
def run(nodetype: str = 'full'):
    """Run node.
    
    :param nodetype: specify node type [full, sol, event, grid]
    """
    worker = h_worker.Worker()
    utils.progress_msg('Starting node(s)')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.run(nodetype))
    # loop.close()


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
def quick(reset: str = 'False',
          nettype: str = 'private'):
    """Quick start. (run a full private/main node by one command)

    :param reset: reset all
    :param nettype: specify net type [main, private]
    """
    utils.logo_shadow()
    init('latest', reset)
    config(nettype, 0, 0, 0, 0, 0, 0, '', '', '', '', 0, 'Null', 'Null', 'Null', 'False')
    run()
    status()


@cbox.cmd
def log(nodetype: str = 'full',
        filter: str = ''):
    """Show filtered log.

    :param nodetype: specify node type [full, sol, event, grid]
    :param filter: specify filter [number/height]
    """
    log = h_log.Log()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(log.show_log(nodetype, filter))
    loop.close()


@cbox.cmd
def version():
    """Check installed troncli version.
    """
    utils.progress_msg('Version:')
    utils.msg(str(__version__))
    utils.info_msg('Upgrade to latest version:')
    utils.msg('pip install troncli --upgrade')


@cbox.cmd
def i():
    """Interactive Mode.
    """
    imode_handler = h_imode.IMode()
    choose_your_poison = { 'version': 'latest',
                           'reset':  'False',
                           'nettype': 'private',
                           'dbname': 'Null',
                           'dbusername': 'Null',
                           'dbpassword': 'Null',
                           'task_queue': []
                         }
    # 
    # start
    utils.progress_msg('Switched to <Interactive Mode>')
    utils.logo_simple()

    utils.imode_msg('Welcome to use troncli interactive mode!')
    """
        init
    """
    utils.imode_msg('If you already initilized and fetched code, you can skip this(init) step by enter [skip], otherwise press any key to continue.')
    _stream = imode_handler.stream()
    if _stream not in ['skip', 'SKIP']:
        # choose java-tron version
        utils.imode_msg('Use latest supported version[' + JAVA_TRON_LASTEST_VERSION + '] of java-tron? [Y(default)/n]')
        _stream = imode_handler.stream()
        if _stream not in ['Y', 'y', 'yes', 'Yes', 'YES', '']:
            utils.imode_msg('ok, so which version you want to use?[3.1.3 - ' + JAVA_TRON_LASTEST_VERSION + ']')
            _stream = imode_handler.stream()
            choose_your_poison['version'] = _stream
        else:
            utils.msg('Y')
        # choose reset
        utils.imode_msg('Reset everything? [y/N(default)]')
        _stream = imode_handler.stream()
        if _stream not in ['N', 'n', 'no', 'No', 'NO', '']:
            choose_your_poison['reset'] = 'True'
        else:
            utils.msg('N')
        #
        # call init
        init(choose_your_poison['version'], choose_your_poison['reset'])
    else:
        utils.imode_msg('Init Skiped!')
    """
        config
    """
    # choose net type
    utils.imode_msg('Setting up a private testnet or sync to mainnet? [private(default)/main]')
    _stream = imode_handler.stream()
    if _stream == 'main':
        choose_your_poison['nettype'] = _stream
    else:
        utils.msg('private')
    # set task_queue
    utils.imode_msg('Do you want set up event services (event-node + tron-gird)? [y/n(default)]')
    _stream = imode_handler.stream()
    if _stream not in ['N', 'n', 'no', 'No', 'NO', '']:
        # set db
        utils.imode_msg('!!! NOTICE: Assume you already installed MongoDB and created user with a role.')
        utils.imode_msg('Enter your db name:')
        _stream = imode_handler.stream()
        choose_your_poison['dbname'] = _stream
        utils.imode_msg('Enter your db user-name:')
        _stream = imode_handler.stream()
        choose_your_poison['dbusername'] = _stream
        utils.imode_msg('Enter your db user-password:')
        _stream = imode_handler.stream()
        choose_your_poison['dbpassword'] = _stream
        # add to task
        choose_your_poison['task_queue'].extend(['event', 'grid'])
        if choose_your_poison['nettype'] == 'private':
            choose_your_poison['task_queue'].extend(['full'])
    else:
        utils.msg('N')
        _node_list = utils.Node()
        _node_list.reset_config()
        choose_your_poison['task_queue'].extend(['full'])

    config(choose_your_poison['nettype'], 0, 0, 0, 0, 0, 0, '', '', '', '', 0,
                              choose_your_poison['dbname'],
                              choose_your_poison['dbusername'],
                              choose_your_poison['dbpassword'],
                              'False')
    """
        run
    """
    while choose_your_poison['task_queue']:
        _nodetype = choose_your_poison['task_queue'].pop(0)
        utils.imode_msg('Press anykey to start ' + _nodetype + '-node? - Enter [exit] to exit.')
        _stream = imode_handler.stream()
        run(_nodetype)
    # utils.debug(str(choose_your_poison))
    #
    # end
    utils.progress_msg('Left <Interactive Mode>')



def main():
    cbox.main([init, config, run, stop, status, quick, log, version, i])


if __name__ == '__main__':
    main()
