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
        utils.info_msg('To stop this node: tron-cli stop --pid ' + str(pid))
        await self.nodes_list(node_type, pid, 'add')

    async def stop(self, pid):
        try:
            subprocess.Popen(["kill", "-15", pid])
        except OSError as err:
            utils.warning_msg('OSError -' + str(err))
        else:
            await self.nodes_list('', int(pid), 'remove')
            utils.success_msg('process: ' + pid + ' is shut down')
            
    async def nodes_list(self, node_type, pid, execution):
        """
        node_type: "full" / "sol"
        pid: int
        execution: "add" / "remove"
        """
        # load or init node list file
        if os.path.isfile(self.root_path + '/' + RUNNING_NODE_LIST_FILE):
            phrase = utils.Phrase()
            running_nodes = phrase.load_json_file(self.root_path + '/' + RUNNING_NODE_LIST_FILE)
        else:
            running_nodes = {'full': [], 'sol': []}
        
        if execution == 'add':
            running_nodes[node_type].append(pid)
        elif execution == 'remove':
            if pid in running_nodes['full']:
                running_nodes['full'].remove(pid)
            elif pid in running_nodes['sol']:
                running_nodes['sol'].remove(pid)
            else:
                utils.warnning_msg('process id: ' + str(pid) + ' not in the running node list')
        else:
            utils.error_msg('wrong execution key word: ' + str(execution))

        with open(self.root_path + '/' + RUNNING_NODE_LIST_FILE, 'w') as file:
             file.write(json.dumps(running_nodes))

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
        else:
            utils.warning_msg('wrong node type')

        return _process.pid
