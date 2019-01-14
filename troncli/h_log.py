import os

from troncli import utils

class Log:
    """handler for filter logs"""
    def __init__(self):
        self.root_path = os.getcwd()

    async def show_log(self, node_type, filter):
        log_path = utils.log_location(self.root_path, node_type)
        # check filter
        if filter == '':
            cmd = 'tail -fn200 ' + log_path
        elif filter == 'height' or filter == 'number':
            cmd = 'tail -fn200 ' + log_path + ' | grep number='
        else:
            utils.warning_msg('invalid filter option')
        try:
            os.system(cmd)
        except OSError as err:
            error_msg('OS Error -' + str(err))
            os.sys.exit()
