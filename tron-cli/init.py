import os
import shutil

from constants import *
from utils import download, success_msg, warnning_msg, msg

class Init(object):
    """handler for init dirs and fetch code"""
    def __init__(self):
        self.root_path = os.getcwd()
        self.nodes_dir = '/tron_nodes'
        self.fullnode_dir = '/fullnode'
        self.soliditynode_dir = '/soliditynode'
        self.fullnode_jar = 'java-tron.jar'
        self.soliditynode_jar = 'SolidityNode.jar'

    def create_dirs(self):
        path = self.root_path
        try:
            os.mkdir(path + self.nodes_dir)
            os.mkdir(path + self.nodes_dir + self.fullnode_dir)
            os.mkdir(path + self.nodes_dir + self.soliditynode_dir)
        except OSError as err:
            warnning_msg('OSError -' + str(err))
        else:
            success_msg('Folders are created:')
            msg(path + '/ ')
            msg('└──' + self.nodes_dir)
            msg('    |---' + self.fullnode_dir)
            msg('    └──--' + self.soliditynode_dir)

    async def fetch_jars(self, version):
        """
        get release url
        """
        url = JAVA_TRON_RELEASES_URL
        if (version == 'lastest'):
            url += 'Odyssey-v' + JAVA_TRON_LASTEST_VERSION
        elif ('3.1.3' <= version <= '3.1.3'):
            url += 'Odyssey-v' + version
        """
        download
        """
        msg('download fullnode jar might take a while')
        await download(self.fullnode_jar, url)
        success_msg('.jar file of Fullnode is successfully downloaded')
        msg('download solidity jar might take a while')
        await download(self.soliditynode_jar, url)
        success_msg('.jar file of Soliditynode is successfully downloaded')

    async def move_jars(self):
        shutil.move(self.root_path + '/' + self.fullnode_jar, 
            self.root_path + self.nodes_dir + self.fullnode_dir + '/full.jar')
        shutil.move(self.root_path + '/' + self.soliditynode_jar, 
            self.root_path + self.nodes_dir + self.soliditynode_dir + '/solidity.jar')
        success_msg('initialization finished')


