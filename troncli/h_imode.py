import os

from troncli import utils

class IMode:
    def stream(self):
        try:
            _stream = input()
            if _stream == 'exit':
                utils.progress_msg('Left <Interactive Mode>')
                exit()
            # utils.debug(_stream)
        except (KeyboardInterrupt):
            utils.progress_msg('Left <Interactive Mode>')
        else:
            return _stream