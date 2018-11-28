import os
import copy

from troncli import utils, json_store
from troncli.constants import *


class Config:
    """handler for setup config files"""

    def __init__(self):
        self.root_path = os.getcwd()
        self.full_config = None
        self.sol_config = None

    async def init(self):
        """
        Load raw json config
        """
        self.full_config = copy.deepcopy(json_store.raw_config)
        self.sol_config = copy.deepcopy(json_store.raw_config)
        utils.success_msg('config initialized')

    async def export(self):
        """
        Export properties config file
        """
        phrase = utils.Phrase()
        _target_file_path_full = self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_CONFIG
        phrase.store_json2properties_to_file(self.full_config, _target_file_path_full)
        utils.success_msg('fullnode config file exported to: ')
        utils.msg(_target_file_path_full)

        _target_file_path_sol = self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOL_CONFIG
        phrase.store_json2properties_to_file(self.sol_config, _target_file_path_sol)
        utils.success_msg('soliditynode config file exported to: ')
        utils.msg(_target_file_path_sol)

    async def set_http_port(self, port_num, node_type):
        if node_type == 'full':
            self.full_config[' node'][' http'][' fullNodePort'] = port_num
            utils.success_msg('full-node http request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'sol':
            self.sol_config[' node'][' http'][' solidityPort'] = port_num
            utils.success_msg('solidity-node request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        else:
            utils.warning_msg('wrong node_type')

    async def set_grpc_port(self, port_num, node_type):
        if node_type == 'full':
            self.full_config[' node'][' rpc'][' port'] = port_num
            self.sol_config[' node'][' trustNode'] = LOCAL_HOST + str(port_num)
            utils.success_msg('full-node grpc request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'sol':
            self.sol_config[' node'][' rpc'][' port'] = port_num
            utils.success_msg('solidity-node grpc request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        else:
            utils.warning_msg('wrong node_type')

    async def set_net_type(self, net_type):
        # msg
        utils.success_msg('net type set to: ')
        utils.msg(net_type)
        # P2P verison
        if net_type == 'main':
            self.full_config[' node'][' p2p'][' version'] = MAINNET_P2P_VERSION
            self.sol_config[' node'][' p2p'][' version'] = MAINNET_P2P_VERSION
        if net_type == 'private':
            self.full_config[' node'][' p2p'][' version'] = PRIVATENET_P2P_VERSION
            self.sol_config[' node'][' p2p'][' version'] = PRIVATENET_P2P_VERSION
        # committee
        if net_type == 'main':
            self.full_config[' committee'][' allowCreationOfContracts'] = MAINNET_ALLOW_CREATION_OF_CONTRACTS
            self.sol_config[' committee'][' allowCreationOfContracts'] = MAINNET_ALLOW_CREATION_OF_CONTRACTS
        if net_type == 'private':
            self.full_config[' committee'][' allowCreationOfContracts'] = PRIVATENET_ALLOW_CREATION_OF_CONTRACTS
            self.sol_config[' committee'][' allowCreationOfContracts'] = PRIVATENET_ALLOW_CREATION_OF_CONTRACTS
        # vm
        if net_type == 'main':
            self.full_config[' vm'][' supportConstant'] = 'false'
            self.sol_config[' vm'][' supportConstant'] = 'false'
        if net_type == 'private':
            self.full_config[' vm'][' supportConstant'] = 'true'
            self.sol_config[' vm'][' supportConstant'] = 'true'
        # block
        if net_type == 'main':
            self.full_config[' block'][' needSyncCheck'] = 'true'
            self.sol_config[' block'][' needSyncCheck'] = 'true'
        if net_type == 'private':
            self.full_config[' block'][' needSyncCheck'] = 'false'
            self.sol_config[' block'][' needSyncCheck'] = 'false'
        # localwitness
        if net_type == 'main':
            self.full_config[' localwitness'] = []
            self.sol_config[' localwitness'] = []
        if net_type == 'private':
            self.full_config[' localwitness'] = ['da146374a75310b9666e834ee4ad0866d6f4035967bfc76217c5a495fff9f0d0']
            self.sol_config[' localwitness'] = ['da146374a75310b9666e834ee4ad0866d6f4035967bfc76217c5a495fff9f0d0']
        # genesis.block
        if net_type == 'main':
            pass
        #     self.full_config[' genesis.block'][' witnesses'] = 
        #     self.sol_config[' genesis.block'][' witnesses'] = 
        if net_type == 'private':
            self.full_config[' genesis.block'][' witnesses'] = [{
                ' address': 'TPL66VK2gCXNCD7EJg9pgJRfqcRazjhUZY',
                ' url': 'http://tronstudio.com',
                ' voteCount': 10000}]
            self.sol_config[' genesis.block'][' witnesses'] = [{
                ' address': 'TPL66VK2gCXNCD7EJg9pgJRfqcRazjhUZY',
                ' url': 'http://tronstudio.com',
                ' voteCount': 10000}]
