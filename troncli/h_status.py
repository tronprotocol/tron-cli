#!/usr/bin/env python3
import psutil
import os
import argparse
import datetime
import socket
import sys

from troncli import utils
from troncli.constants import *

ACCESS_DENIED = ''
NON_VERBOSE_ITERATIONS = 6


class Status(object):
    def __init__(self):
        self.root_path = os.getcwd()
        self.phrase = utils.Phrase()
        self.node_list = utils.Node()

    def overall(self):
        utils.recommandation()
        virt = psutil.virtual_memory()
        swap = psutil.swap_memory()
        templ = '%-7s %10s %10s %10s %10s %10s %10s'
        utils.status_msg_div()
        utils.status_msg('RAM', '<usages>')
        print(templ % (
                       '', 'total', 'percent', 'used', 'free',
                       'active', 'inactive'))
        print(templ % (
            'Mem:',
            self.phrase.convert_bytes(int(virt.total)),
            str(virt.percent)+'%',
            self.phrase.convert_bytes(int(virt.used)),
            self.phrase.convert_bytes(int(virt.free)),
            self.phrase.convert_bytes(int(virt.active)),
            self.phrase.convert_bytes(int(virt.inactive)))
        )
        print(templ % (
            'Swap:',
            self.phrase.convert_bytes(int(swap.total)),
            str(swap.percent)+'%',
            self.phrase.convert_bytes(int(swap.used)),
            self.phrase.convert_bytes(int(swap.free)),
            '',
            '')
        )
        self.running_nodes()
        self.show_config()
        utils.status_msg_div()
        utils.node_instruction()

    def show_config(self):
        _node_list = self.node_list.get()
        _config = _node_list['config']
        if _config == {}:
            utils.warning_msg('not configurate yet, please check config help by')
            utils.msg('tron-cli config -h')
        else:
            utils.status_msg('Config CMD', 'tron-cli config ' +
                                    '--nettype ' + str(_config['nettype']) + ' '
                                    '--fullhttpport ' + str(_config['fullhttpport']) + ' '
                                    '--solhttpport ' + str(_config['solhttpport']) + ' '
                                    '--eventhttpport ' + str(_config['eventhttpport']) + ' '
                                    '--fullrpcport ' + str(_config['fullrpcport']) + ' '
                                    '--solrpcport ' + str(_config['solrpcport']) + ' '
                                    '--eventrpcport ' + str(_config['eventrpcport']) + ' '
                                    '--enablememdb ' + str(_config['enablememdb']) + ' '
                                    '--dbsyncmode ' + str(_config['dbsyncmode']) + ' '
                                    '--saveintertx ' + str(_config['saveintertx']) + ' '
                                    '--savehistorytx ' + str(_config['savehistorytx']) + ' '
                                    '--gridport ' + str(_config['gridport']) + ' '
                                    '--dbname ' + str(_config['dbname']) + ' '
                                    '--dbusername ' + str(_config['dbusername']) + ' '
                                    '--dbpassword ' + str(_config['dbpassword']))
            if _config['nettype'] == 'private':
                utils.status_msg('Witness Address', TEST_ACCOUNT_ADDRESS)
                utils.status_msg('Witness Private-key', TEST_ACCOUNT_PK)


    def running_nodes(self):
        if os.path.isfile(self.root_path + '/' + RUNNING_NODE_LIST_FILE):
            running_nodes = self.node_list.get()
            utils.status_msg('Node Version', running_nodes['live']['version'])
            utils.status_msg('Full-node IDs', running_nodes['live']['full'])
            if running_nodes['live']['full'] != []:
                utils.msg('http connection: ' + LOCAL_HOST + str(running_nodes['config']['fullhttpport']))
                utils.msg('rpc connection: ' + LOCAL_HOST + str(running_nodes['config']['fullrpcport']))
                utils.msg('log location: ' + utils.log_location(self.root_path, 'full'))
            utils.status_msg('Solidity-node IDs', running_nodes['live']['sol'])
            if running_nodes['live']['sol'] != []:
                utils.msg('http connection: ' + LOCAL_HOST + str(running_nodes['config']['solhttpport']))
                utils.msg('rpc connection: ' + LOCAL_HOST + str(running_nodes['config']['solrpcport']))
                utils.msg('log location: ' + utils.log_location(self.root_path, 'sol'))
            utils.status_msg('Event-node IDs', running_nodes['live']['event'])
            if running_nodes['live']['event'] != []:
                utils.msg('http connection: ' + LOCAL_HOST + str(running_nodes['config']['eventhttpport']))
                utils.msg('rpc connection: ' + LOCAL_HOST + str(running_nodes['config']['eventrpcport']))
            utils.status_msg('Grid-ap IDs', running_nodes['live']['grid'])
            if running_nodes['live']['grid'] != []:
                utils.msg('http connection: ' + LOCAL_HOST + str(running_nodes['config']['gridport']))
        else:
            utils.warning_msg('no running nodes')

    def str_ntuple(self, nt, bytes2human=False):
        if nt == ACCESS_DENIED:
            return ''
        if not bytes2human:
            return ', '.join(['%s=%s' % (x, getattr(nt, x))
                             for x in nt._fields])
        else:
            return ', '.join(['%s=%s' %
                             (x, self.phrase.convert_bytes(getattr(nt, x)))
                             for x in nt._fields])

    def ps(self, pid, verbose=False):
        try:
            proc = psutil.Process(pid)
            pinfo = proc.as_dict(ad_value=ACCESS_DENIED)
        except psutil.NoSuchProcess as err:
            sys.exit(str(err))

        # collect other proc info
        with proc.oneshot():
            try:
                parent = proc.parent()
                if parent:
                    parent = '(%s)' % parent.name()
                else:
                    parent = ''
            except psutil.Error:
                parent = ''
            try:
                pinfo['children'] = proc.children()
            except psutil.Error:
                pinfo['children'] = []
            if pinfo['create_time']:
                started = datetime.datetime.fromtimestamp(
                    pinfo['create_time']).strftime('%Y-%m-%d %H:%M')
            else:
                started = ACCESS_DENIED

        # details:
        utils.status_msg('pid', pinfo['pid'])
        utils.status_msg('name', pinfo['name'])
        utils.status_msg('exe', pinfo['exe'])
        utils.status_msg('cwd', pinfo['cwd'])
        utils.status_msg('cmdline', ' '.join(pinfo['cmdline']))
        utils.status_msg('started', started)

        cpu_tot_time = datetime.timedelta(seconds=sum(pinfo['cpu_times']))
        cpu_tot_time = '%s:%s.%s' % (
            cpu_tot_time.seconds // 60 % 60,
            str((cpu_tot_time.seconds % 60)).zfill(2),
            str(cpu_tot_time.microseconds)[:2])
        utils.status_msg('cpu-tspent', cpu_tot_time)
        utils.status_msg('cpu-times', self.str_ntuple(pinfo['cpu_times']))
        if hasattr(proc, 'cpu_affinity'):
            utils.status_msg('cpu-affinity', pinfo['cpu_affinity'])
        if hasattr(proc, 'cpu_num'):
            utils.status_msg('cpu-num', pinfo['cpu_num'])

        utils.status_msg('memory', self.str_ntuple(pinfo['memory_info'],
                         bytes2human=True))
        utils.status_msg('memory %', round(pinfo['memory_percent'], 2))
        utils.status_msg('user', pinfo['username'])
        utils.status_msg('status', pinfo['status'])

        utils.status_msg('num-threads', pinfo['num_threads'])
        if psutil.POSIX:
            utils.status_msg('num-fds', pinfo['num_fds'])
        if psutil.WINDOWS:
            utils.status_msg('num-handles', pinfo['num_handles'])

        if 'io_counters' in pinfo:
            utils.status_msg('I/O', self.str_ntuple(pinfo['io_counters'],
                             bytes2human=True))
        if 'num_ctx_switches' in pinfo:
            utils.status_msg('ctx-switches',
                             self.str_ntuple(pinfo['num_ctx_switches']))
        if pinfo['children']:
            template = '%-6s %s'
            utils.status_msg('children', template % ('PID', 'NAME'))
            for child in pinfo['children']:
                try:
                    utils.status_msg('', template % (child.pid, child.name()))
                except psutil.AccessDenied:
                    utils.status_msg('', template % (child.pid, ''))
                except psutil.NoSuchProcess:
                    pass

        if pinfo['open_files']:
            utils.status_msg('open-files', 'PATH')
            for i, file in enumerate(pinfo['open_files']):
                if not verbose and i >= NON_VERBOSE_ITERATIONS:
                    utils.status_msg('', '[...]')
                    break
                utils.status_msg('', file.path)
        else:
            utils.status_msg('open-files', '')

        if pinfo['connections']:
            template = '%-5s %-25s %-25s %s'
            utils.status_msg('connections', template %
                             ('PROTO', 'LOCAL ADDR', 'REMOTE ADDR', 'STATUS'))
            for conn in pinfo['connections']:
                if conn.type == socket.SOCK_STREAM:
                    type = 'TCP'
                elif conn.type == socket.SOCK_DGRAM:
                    type = 'UDP'
                else:
                    type = 'UNIX'
                lip, lport = conn.laddr
                if not conn.raddr:
                    rip, rport = '*', '*'
                else:
                    rip, rport = conn.raddr
                utils.status_msg('', template % (
                    type,
                    '%s:%s' % (lip, lport),
                    '%s:%s' % (rip, rport),
                    conn.status))
        else:
            utils.status_msg('connections', '')

        if hasattr(proc, 'environ') and pinfo['environ']:
            template = '%-25s %s'
            utils.status_msg('environ', template % ('NAME', 'VALUE'))
            for i, k in enumerate(sorted(pinfo['environ'])):
                if not verbose and i >= NON_VERBOSE_ITERATIONS:
                    utils.status_msg('', '[...]')
                    break
                utils.status_msg('', template % (k, pinfo['environ'][k]))

        if pinfo.get('memory_maps', None):
            template = '%-8s %s'
            utils.status_msg('mem-maps', template % ('RSS', 'PATH'))
            maps = sorted(pinfo['memory_maps'], key=lambda x: x.rss,
                          reverse=True)
            for i, region in enumerate(maps):
                if not verbose and i >= NON_VERBOSE_ITERATIONS:
                    utils.status_msg('', '[...]')
                    break
                utils.status_msg('', template %
                                 (self.phrase.convert_bytes(region.rss),
                                  region.path))
