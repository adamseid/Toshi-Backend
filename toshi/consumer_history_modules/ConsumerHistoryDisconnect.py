from ..models import HistoryConnections
from . import Misc

FILE_NAME = 'Disconnect'
DEBUG = True
STATE_CSV_PATH = './toshi/state/top_performer.csv'


def clearConnections(self):
    room_group_name = self.room_group_name
    print("SENT ROOM GROUP NAME: ", room_group_name)
    HistoryConnections.objects.filter(roomGroupName=room_group_name).delete()


def clearStateCSV(self):
    FUNCTION_NAME = 'clearStateCSV'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    clearConnections(self)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run(self):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    clearStateCSV(self)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)