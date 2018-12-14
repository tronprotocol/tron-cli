import os
import copy
import shutil

from troncli import utils, json_store
from troncli.constants import *


class Config:
    """handler for setup config files"""

    def __init__(self):
        self.root_path = os.getcwd()
        self.full_config = None
        self.sol_config = None
        self.event_config = None
        self.enable_event_services = False
        self.node_list = utils.Node()
        self.phrase = utils.Phrase()

    async def init(self):
        """
        Load raw json config
        """
        self.full_config = copy.deepcopy(json_store.raw_config)
        self.sol_config = copy.deepcopy(json_store.raw_config)
        self.event_config = copy.deepcopy(json_store.raw_config)
        self.eventnode_db_properties = copy.deepcopy(json_store.raw_eventnode_mongodb_properties)
        self.gridapi_db_properties = copy.deepcopy(json_store.raw_gridapi_application_properties)
        utils.success_msg('config initialized')

    async def export(self):
        """
        Export properties config file
        """
        _target_file_path_full = self.root_path + NODES_DIR + FULL_NODE_DIR + FULL_CONFIG
        self.phrase.store_json2properties_to_file(self.full_config, _target_file_path_full)
        utils.success_msg('fullnode config file exported to: ')
        utils.msg(_target_file_path_full)

        _target_file_path_sol = self.root_path + NODES_DIR + SOLIDITY_NODE_DIR + SOL_CONFIG
        self.phrase.store_json2properties_to_file(self.sol_config, _target_file_path_sol)
        utils.success_msg('soliditynode config file exported to: ')
        utils.msg(_target_file_path_sol)

        _target_file_path_sol = self.root_path + NODES_DIR + EVENT_NODE_DIR + EVENT_CONFIG
        self.phrase.store_json2properties_to_file(self.event_config, _target_file_path_sol)
        utils.success_msg('eventnode config file exported to: ')
        utils.msg(_target_file_path_sol)

    async def set_http_port(self, port_num, node_type, net_type):
        if node_type == 'full':
            self.full_config[' node'][' http'][' fullNodePort'] = port_num
            if net_type == 'private':
                self.event_config[' seed.node'][' ip.list'] = [LOCAL_HOST + ':' + str(port_num)]
                self.event_config[' node'][' active'] = [LOCAL_HOST + ':' + str(port_num)]
            utils.success_msg('full-node http request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'sol':
            self.sol_config[' node'][' http'][' solidityPort'] = port_num
            utils.success_msg('solidity-node request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'event':
            self.event_config[' node'][' http'][' fullNodePort'] = port_num
            utils.success_msg('event-node request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        else:
            utils.warning_msg('wrong node_type')

    async def set_rpc_port(self, port_num, node_type):
        if node_type == 'full':
            self.full_config[' node'][' rpc'][' port'] = port_num
            self.sol_config[' node'][' trustNode'] = LOCAL_HOST + str(port_num)
            utils.success_msg('full-node rpc request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'sol':
            self.sol_config[' node'][' rpc'][' port'] = port_num
            utils.success_msg('solidity-node rpc request set to listen: ')
            utils.msg(LOCAL_HOST + str(port_num))
        elif node_type == 'event':
            self.event_config[' node'][' rpc'][' port'] = port_num
            utils.success_msg('event-node rpc request set to listen: ')
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
            self.event_config[' node'][' p2p'][' version'] = MAINNET_P2P_VERSION
        if net_type == 'private':
            self.full_config[' node'][' p2p'][' version'] = PRIVATENET_P2P_VERSION
            self.sol_config[' node'][' p2p'][' version'] = PRIVATENET_P2P_VERSION
            self.event_config[' node'][' p2p'][' version'] = PRIVATENET_P2P_VERSION
        # committee
        if net_type == 'main':
            self.full_config[' committee'][' allowCreationOfContracts'] = MAINNET_ALLOW_CREATION_OF_CONTRACTS
            self.sol_config[' committee'][' allowCreationOfContracts'] = MAINNET_ALLOW_CREATION_OF_CONTRACTS
            self.event_config[' committee'][' allowCreationOfContracts'] = MAINNET_ALLOW_CREATION_OF_CONTRACTS
        if net_type == 'private':
            self.full_config[' committee'][' allowCreationOfContracts'] = PRIVATENET_ALLOW_CREATION_OF_CONTRACTS
            self.sol_config[' committee'][' allowCreationOfContracts'] = PRIVATENET_ALLOW_CREATION_OF_CONTRACTS
            self.event_config[' committee'][' allowCreationOfContracts'] = PRIVATENET_ALLOW_CREATION_OF_CONTRACTS
        # vm
        if net_type == 'main':
            self.full_config[' vm'][' supportConstant'] = 'false'
            self.sol_config[' vm'][' supportConstant'] = 'false'
            self.event_config[' vm'][' supportConstant'] = 'false'
        if net_type == 'private':
            self.full_config[' vm'][' supportConstant'] = 'true'
            self.sol_config[' vm'][' supportConstant'] = 'true'
            self.event_config[' vm'][' supportConstant'] = 'true'
        # block
        if net_type == 'main':
            self.full_config[' block'][' needSyncCheck'] = 'true'
            self.sol_config[' block'][' needSyncCheck'] = 'true'
            self.event_config[' block'][' needSyncCheck'] = 'true'
        if net_type == 'private':
            self.full_config[' block'][' needSyncCheck'] = 'false'
            self.sol_config[' block'][' needSyncCheck'] = 'false'
            self.event_config[' block'][' needSyncCheck'] = 'false'
        # localwitness
        if net_type == 'main':
            self.full_config[' localwitness'] = []
            self.sol_config[' localwitness'] = []
            self.event_config[' localwitness'] = []
        if net_type == 'private':
            self.full_config[' localwitness'] = ['da146374a75310b9666e834ee4ad0866d6f4035967bfc76217c5a495fff9f0d0']
            self.sol_config[' localwitness'] = ['da146374a75310b9666e834ee4ad0866d6f4035967bfc76217c5a495fff9f0d0']
            self.event_config[' localwitness'] = ['da146374a75310b9666e834ee4ad0866d6f4035967bfc76217c5a495fff9f0d0']
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
            self.event_config[' genesis.block'][' witnesses'] = [{
                ' address': 'TPL66VK2gCXNCD7EJg9pgJRfqcRazjhUZY',
                ' url': 'http://tronstudio.com',
                ' voteCount': 10000}]

    async def set_db_version(self, enablememdb):
        if enablememdb == 'disable' or enablememdb == '0' or enablememdb == 'False':
            # enablememdb = False
            self.full_config[' storage'][' db.version'] = DB_DISK_ONLY_VERSION
            self.event_config[' storage'][' db.version'] = DB_DISK_ONLY_VERSION
            utils.success_msg('enable in memeory db:')
            utils.msg('False')
        else:
            # enablememdb = True
            self.full_config[' storage'][' db.version'] = DB_IN_MEMORY_SUPPORT_VERSION
            self.event_config[' storage'][' db.version'] = DB_IN_MEMORY_SUPPORT_VERSION
            utils.success_msg('enable in memeory db:')
            utils.msg('True')

    async def store_db_settings(self, dbname, dbusername, dbpassword, gridport):
        if dbname == 'Null' and dbusername == 'Null' and dbpassword == 'Null':
            self.enable_event_services = False
            utils.warning_msg('Not configing event services since db settings not specified.')
        elif dbname == 'Null':
            utils.error_msg('Please set db name with --dbname')
            exit()
        elif dbusername == 'Null':
            utils.error_msg('Please set db user name with --dbusername')
            exit()
        elif dbpassword == 'Null':
            utils.error_msg('Please set db password with --dbpassword')
            exit()
        else:
            self.enable_event_services = True
            await self.node_list.update_db_settings(dbname, dbusername, dbpassword)
            utils.success_msg('db settings stored')
            await self.change_eventnode_db_settings()
            await self.change_gridapi_db_settings(gridport)
            await self.build_eventnode_jar()

    async def change_eventnode_db_settings(self):
        _db = await self.node_list.get()
        # utils.debug(str(_db['db']))
        self.eventnode_db_properties[' mongo.dbname'] = _db['db']['dbname']
        self.eventnode_db_properties[' mongo.username'] = _db['db']['dbusername']
        self.eventnode_db_properties[' mongo.password'] = _db['db']['dbpassword']
        """
        export
        """
        _target_file_path_sol = self.root_path + NODES_DIR + EVENT_NODE_DIR + '/src/main/resources/mongodb.properties'
        self.phrase.store_json2javabeanconfig_to_file(self.eventnode_db_properties, _target_file_path_sol)
        utils.success_msg('changed db settings for event node at: ')
        utils.msg(_target_file_path_sol)

    async def change_gridapi_db_settings(self, gridport):
        _db = await self.node_list.get()
        # utils.debug(str(_db['db']))
        self.gridapi_db_properties[' spring.data.mongodb.database'] = _db['db']['dbname']
        self.gridapi_db_properties[' spring.data.mongodb.username'] = _db['db']['dbusername']
        self.gridapi_db_properties[' spring.data.mongodb.password'] = _db['db']['dbpassword']
        self.gridapi_db_properties[' server.port'] = gridport
        utils.success_msg('grid api request set to listen: ')
        utils.msg(LOCAL_HOST + str(gridport))
        """
        export
        """
        _target_file_path_sol = self.root_path + NODES_DIR + GRID_API_DIR + '/src/main/resources/application.properties'
        self.phrase.store_json2javabeanconfig_to_file(self.gridapi_db_properties, _target_file_path_sol)
        utils.success_msg('changed db settings for grid api at: ')
        utils.msg(_target_file_path_sol)

    async def build_eventnode_jar(self):
        utils.progress_msg('Build event node jar')
        os.chdir(self.root_path + NODES_DIR + EVENT_NODE_DIR)
        await utils.gradlew_build('event node')
        os.chdir(self.root_path)
        shutil.move(self.root_path + NODES_DIR + EVENT_NODE_DIR + '/build/libs/FullNode.jar',
                    self.root_path + NODES_DIR + EVENT_NODE_DIR + EVENT_NODE_JAR)
        utils.success_msg('event node jar move to:')
        utils.msg(self.root_path + NODES_DIR + EVENT_NODE_DIR + EVENT_NODE_JAR)

