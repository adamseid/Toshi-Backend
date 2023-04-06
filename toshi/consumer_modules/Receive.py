from . import Misc
from .receive import Select

FILE_NAME = 'Receive'
DEBUG = True


def run(self, data):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    if data['request'] == 'select':
        print('select')
        Select.run(self, data)

    

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
