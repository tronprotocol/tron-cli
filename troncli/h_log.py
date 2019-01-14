import os

from troncli import utils

class Log:
    """handler for filter logs"""
    def __init__(self):
        self.root_path = os.getcwd()

    async def show_full_log(self, node_type):
        log_path = utils.log_location(self.root_path, node_type)
        cmd = 'tail -fn200 ' + log_path
        try:
            os.system(cmd)
        except OSError as err:
            error_msg('OS Error -' + str(err))
            os.sys.exit()

    async def show_block_num(self, node_type):
        log_path = utils.log_location(self.root_path, node_type)
        cmd = 'tail -fn200 ' + log_path + ' | grep number='
        try:
            os.system(cmd)
        except OSError as err:
            error_msg('OS Error -' + str(err))
            os.sys.exit()
