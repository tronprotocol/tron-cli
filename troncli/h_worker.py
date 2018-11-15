import os
import subprocess

from troncli import utils
from troncli.constants import *

class Worker(object):
    """handler for manage multiple nodes in multiple processes"""
    def __init__(self):
        self.root_path = os.getcwd()
        self.processes = {}

    async def run(self, node_type):
        # self.processes['fullnode'] = self.start()
        pid = await self.start(node_type)
        utils.success_msg('node running at pid:' + str(pid))

    async def start(self, node_type):
        """
        start a node and return its pid
        execute cmd to inherit the shell process, instead of having the shell launch a child process
        """
        if node_type == 'full':
            os.chdir(self.root_path + NODES_DIR + FULL_NODE_DIR)

            cmd = "java -jar " + self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_NODE_JAR + \
                " -c " + self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_CONFIG + " --witness" + \
                " -d " + self.root_path + NODES_DIR + FULL_NODE_DIR + "/data"

            _process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

            os.chdir(self.root_path + NODES_DIR)
        elif node_type == 'sol':
            os.chdir(self.root_path + NODES_DIR + SOLIDITY_NODE_DIR)

            cmd = "java -jar " + self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOLIDITY_NODE_JAR + \
                " -c " + self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOL_CONFIG + " --witness" + \
                " -d " + self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + "/data"

            _process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

            os.chdir(self.root_path + NODES_DIR)
        else:
            utils.warnning_msg('wrong node type')

        return _process.pid

    async def stop(self, pid):
        try:
            subprocess.Popen(["kill", "-15", pid])
        except OSError as err:
            utils.warnning_msg('OSError -' + str(err))
        else:
            utils.success_msg('process: ' + pid + ' is shutting down')

        
