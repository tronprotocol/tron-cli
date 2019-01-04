import os
import subprocess
import json
import copy

from troncli import utils
from troncli.constants import *


class Worker:
    """handler for manage multiple nodes in multiple processes"""

    def __init__(self):
        self.root_path = os.getcwd()
        self.processes = {}
        self.node_list = utils.Node()

    async def run(self, node_type):
        pid = await self.run_node(node_type)
        utils.success_msg('node running at pid:')
        _config = self.node_list.get()['config']
        utils.msg(str(pid))
        utils.status_msg('HTTP', LOCAL_HOST + str(_config[node_type + 'httpport']))
        utils.status_msg('RPC', LOCAL_HOST + str(_config[node_type + 'rpcport']))
        utils.status_msg('LOG PATH', utils.log_location(self.root_path, node_type))
        utils.node_cmds(pid)
        await self.node_list.update_running_node(node_type, pid, 'add')

    async def stop(self, node):
        if node == 'all':
            _c = copy.deepcopy(self.node_list.get())
            all_nodes = _c['live']['all']
            if all_nodes != []:
                utils.progress_msg('Shutting down node(s)')
            else:
                utils.warning_msg('no running nodes')
            while all_nodes != []:
                _node = all_nodes.pop(-1)
                await self.stop_node(str(_node))
        else:
            utils.progress_msg('Shutting down node(s)')
            await self.stop_node(node)

    async def stop_node(self, node_id):
        try:
            subprocess.Popen(["kill", "-15", node_id])
        except OSError as err:
            utils.warning_msg('OSError -' + str(err))
        else:
            await self.node_list.update_running_node('', int(node_id), 'remove')
            utils.success_msg('process: ' + node_id + ' is shut down')

    async def run_node(self, node_type):
        """
        start a node and return its pid
        execute cmd to inherit the shell process, instead of having the shell launch a child process
        """
        global _process
        if node_type == 'full':
            os.chdir(self.root_path + NODES_DIR + FULL_NODE_DIR)

            cmd = "java -jar " + self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_NODE_JAR + \
                  " -c " + self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_CONFIG + " --witness" + \
                  " -d " + self.root_path + NODES_DIR + FULL_NODE_DIR + "/data"

            _process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

            os.chdir(self.root_path)
        elif node_type == 'sol':
            os.chdir(self.root_path + NODES_DIR + SOLIDITY_NODE_DIR)

            cmd = "java -jar " + self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOLIDITY_NODE_JAR + \
                  " -c " + self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOL_CONFIG + " --witness" + \
                  " -d " + self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + "/data"

            _process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

            os.chdir(self.root_path)
        elif node_type == 'event':
            os.chdir(self.root_path + NODES_DIR + EVENT_NODE_DIR)

            cmd = "java -jar " + self.root_path + NODES_DIR + EVENT_NODE_DIR + EVENT_NODE_JAR + \
                  " -c " + self.root_path + NODES_DIR + EVENT_NODE_DIR + EVENT_CONFIG + " --witness" + \
                  " -d " + self.root_path + NODES_DIR + EVENT_NODE_DIR + "/data"

            _process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

            os.chdir(self.root_path)
        elif node_type == 'grid':
            os.chdir(self.root_path + NODES_DIR + GRID_API_DIR)

            subprocess.call(['mvn', 'package'])

            cmd = "java -jar target/trongrid-1.0.1-SNAPSHOT.jar"
            # _process = subprocess.Popen(cmd)
            _process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

            os.chdir(self.root_path)
        else:
            utils.warning_msg('wrong node type')

        return _process.pid
