from ....models import OverviewConnections
from ... import Misc
import pandas as pd

FILE_NAME = 'Dashboard'
DEBUG = True
STATE_CSV_PATH = './toshi/state/top_performer.csv'


def getConnectionStatus(self, state_csv):
    FUNCTION_NAME = 'getConnectionStatus'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    connection_status = 'not-connected'
    for room_group_name in state_csv['roomGroupName']:
        if room_group_name == self.room_group_name:
            connection_status = 'connected'
        else:
            pass
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
    return connection_status


def getStatusIndex(self, state_csv):
    for i in range(len(state_csv)):
        if self.room_group_name == state_csv['roomGroupName'][i]:
            return i


def updateStateCSV(self, data):
    FUNCTION_NAME = 'updateStateCSV'
    OverviewConnections.objects.filter(roomGroupName=self.room_group_name).update(timeFrame = data['time_frame'])
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run(self, data):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    updateStateCSV(self, data)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
