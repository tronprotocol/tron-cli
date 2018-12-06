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

    def overall(self):
        virt = psutil.virtual_memory()
        swap = psutil.swap_memory()
        templ = '%-7s %10s %10s %10s %10s %10s %10s %10s'
        print(templ % (
                       '', 'total', 'percent', 'used', 'free',
                       'active', 'inactive', 'wired'))
        print(templ % (
            'Mem:',
            self.phrase.convert_bytes(int(virt.total)),
            str(virt.percent)+'%',
            self.phrase.convert_bytes(int(virt.used)),
            self.phrase.convert_bytes(int(virt.free)),
            self.phrase.convert_bytes(int(virt.active)),
            self.phrase.convert_bytes(int(virt.inactive)),
            self.phrase.convert_bytes(int(virt.wired)))
        )
        print(templ % (
            'Swap:',
            self.phrase.convert_bytes(int(swap.total)),
            str(swap.percent)+'%',
            self.phrase.convert_bytes(int(swap.used)),
            self.phrase.convert_bytes(int(swap.free)),
            '',
            '',
            '')
        )
        self.running_nodes()

    def running_nodes(self):
        if os.path.isfile(self.root_path + '/' + RUNNING_NODE_LIST_FILE):
            phrase = utils.Phrase()
            running_nodes = phrase.load_json_file(self.root_path + '/' +
                                                  RUNNING_NODE_LIST_FILE)
            utils.status_msg('Full-nodes', running_nodes['full'])
            utils.status_msg('Solidity-nodes', running_nodes['sol'])
            utils.info_msg('To stop node: tron-cli stop --pid')
        else:
            utils.warnning_msg('no running nodes')

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
