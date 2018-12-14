import os
import subprocess
import json

from troncli import utils
from troncli.constants import *


class Worker:
    """handler for manage multiple nodes in multiple processes"""

    def __init__(self):
        self.root_path = os.getcwd()
        self.processes = {}

    async def run(self, node_type):
        pid = await self.start(node_type)
        utils.success_msg('node running at pid:')
        utils.msg(str(pid))
        utils.info_msg('To stop this node:')
        utils.msg('tron-cli stop --pid ' + str(pid))
        utils.info_msg('To check node running details:')
        utils.msg('tron-cli status --node ' + str(pid))
        node_list = utils.Node()
        await node_list.update_running_node(node_type, pid, 'add')

    async def stop(self, pid):
        try:
            subprocess.Popen(["kill", "-15", pid])
        except OSError as err:
            utils.warning_msg('OSError -' + str(err))
        else:
            node_list = utils.Node()
            await node_list.update_running_node('', int(pid), 'remove')
            utils.success_msg('process: ' + pid + ' is shut down')

    async def start(self, node_type):
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
