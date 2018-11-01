import os
import shutil

from constants import *
from utils import download

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
        print('[TRON-CLI]: Creating foldres...')
        try:
            os.mkdir(path + self.nodes_dir)
            os.mkdir(path + self.nodes_dir + self.fullnode_dir)
            os.mkdir(path + self.nodes_dir + self.soliditynode_dir)
        except OSError as err:
            print('✖: OSError: ', err)
        else:
            print('✓: Folders are created under the root:')
            print('    ' + path + '/ ')
            print('    ' + self.nodes_dir)
            print('     |---' + self.fullnode_dir)
            print('     |---' + self.soliditynode_dir)

    async def fetch_jars(self, version):
        # https://github.com/tronprotocol/java-tron/releases/download/Odyssey-v3.1.3/java-tron.jar
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
        print('[TRON-CLI]: Download release builds...')
        await download(self.fullnode_jar, url)
        print('✓: .jar file of Fullnode is successfully downloaded')
        await download(self.soliditynode_jar, url)
        print('✓: .jar file of Soliditynode is successfully downloaded')

    async def move_jars(self):
        shutil.move(self.root_path + '/' + self.fullnode_jar, 
            self.root_path + self.nodes_dir + self.fullnode_dir + '/full.jar')
        shutil.move(self.root_path + '/' + self.soliditynode_jar, 
            self.root_path + self.nodes_dir + self.soliditynode_dir + '/solidity.jar')
        print('✓: initialization finished')


