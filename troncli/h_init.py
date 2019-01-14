import os
import re
import shutil
import subprocess

from troncli import utils
from troncli.constants import *


class Init(object):
    """handler for init dirs and fetch code"""

    def __init__(self):
        self.root_path = os.getcwd()
        self.source_full_jar = 'FullNode.jar'
        self.source_sol_jar = 'SolidityNode.jar'
        self.event_node_zip = 'event_parser.zip'
        self.tron_grid_zip = ''
        self.node_list = utils.Node()

    async def env_check(self):
        try:
            jdk_version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
            jdk_version = re.search('\"(\d+\.\d+).*\"', str(jdk_version)).groups()[0]
        except OSError as err:
            utils.warning_msg('OS Warning -' + str(err))
            utils.error_msg('Please make sure you install Oracle JDK 1.8 correctly.')
            os.sys.exit()
        else:
            if jdk_version != '1.8':
                utils.error_msg('java-tron required Oracle JDK version = 1.8, please install and use JDK 1.8')
                os.sys.exit()

    async def create_dirs(self, reset):
        path = self.root_path
        """
        reset folders
        """
        if reset == 'True' or reset == 'yes' or reset == '1' or reset == 'on':
            try:
                shutil.rmtree(path + NODES_DIR)
            except OSError as err:
                utils.warning_msg('OS Warning -' + str(err))
            else:
                utils.success_msg('Folders reset.')

        try:
            os.mkdir(path + NODES_DIR)
            os.mkdir(path + NODES_DIR + FULL_NODE_DIR)
            os.mkdir(path + NODES_DIR + SOLIDITY_NODE_DIR)
            os.mkdir(path + NODES_DIR + EVENT_NODE_DIR)
            os.mkdir(path + NODES_DIR + GRID_API_DIR)
        except OSError as err:
            utils.warning_msg('OS Warning -' + str(err))
        else:
            utils.success_msg('Folders are created:')
            utils.msg(path + '/ ')
            utils.msg('└──' + NODES_DIR)
            utils.msg('    ├──' + FULL_NODE_DIR)
            utils.msg('    ├──' + SOLIDITY_NODE_DIR)
            utils.msg('    ├──' + EVENT_NODE_DIR)
            utils.msg('    └──' + GRID_API_DIR)

    async def fetch_code(self):
        """
        get event parser/node and tron-grid code and unzip
        """
        """
        event node
        """
        try:
            await utils.git_clone(JAVA_TRON_EVENT_NODE_GIT_URL,
                        JAVA_TRON_EVENT_NODE_BRANCH_NAME,
                        self.root_path + NODES_DIR + EVENT_NODE_DIR)
        except OSError as err:
            utils.warning_msg('OS Warning -' + str(err))
        else:
            utils.success_msg('event-node source code cloned')
        """
        tron-grid
        """
        try:
            await utils.git_clone(TRON_GRID_GIT_URL,
                        TRON_GRID_BRANCH_NAME,
                        self.root_path + NODES_DIR + GRID_API_DIR)
        except OSError as err:
            utils.warning_msg('OS Warning -' + str(err))
        else:
            utils.success_msg('tron-grid source code cloned')

    async def fetch_jars(self, version):
        """
        get release url
        """
        url = JAVA_TRON_RELEASES_URL
        if version == 'latest':
            url += 'Odyssey-v' + JAVA_TRON_LASTEST_VERSION
            await self.node_list.update_node_version(JAVA_TRON_LASTEST_VERSION)
        elif '3.1.3' <= version <= '3.1.3':
            url += 'Odyssey-v' + version
            self.source_full_jar = 'java-tron.jar'
            await self.node_list.update_node_version(version)
        elif '3.2.0' <= version <= '3.2.10':
            url += 'Odyssey-v' + version
            await self.node_list.update_node_version(version)
        else:
            utils.error_msg('version: ' + version + ' not supported')
            utils.info_msg('current support versions: 3.1.3, 3.2, 3.2.1')
            exit()
        """
        download
        """
        utils.progress_msg('Downloading full-node jar from released build')
        await utils.download(self.source_full_jar, url)
        utils.success_msg('.jar file of Fullnode is successfully downloaded')

        utils.progress_msg('Downloading solidity-node jar from released build')
        await utils.download(self.source_sol_jar, url)
        utils.success_msg('.jar file of Soliditynode is successfully downloaded')

    async def move_jars(self):
        shutil.move(self.root_path + '/' + self.source_full_jar,
                    self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_NODE_JAR)
        shutil.move(self.root_path + '/' + self.source_sol_jar,
                    self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOLIDITY_NODE_JAR)
        utils.success_msg('initialization finished')
