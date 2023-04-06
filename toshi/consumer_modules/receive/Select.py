from .. import Misc
from .select import TopPerformers, DailyTopPerformer, Header

FILE_NAME = 'Select'
DEBUG = True
STATE_CSV_PATH = './trading_bot/state/update_frontend.csv'


def run(self, data):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    print(data)
    if data['location'][0] == 'header':
        Header.run(self, data)
    elif data['location'][1] == 'top-performers':
        TopPerformers.run(self, data)
    elif data['location'][1] == 'daily-top-performers':
        DailyTopPerformer.run(self, data)


    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
