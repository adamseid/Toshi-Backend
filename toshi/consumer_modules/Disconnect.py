from ..models import OverviewConnections, ProfileConnections
from . import Misc
import pandas as pd

FILE_NAME = 'Disconnect'
DEBUG = True
STATE_CSV_PATH = './toshi/state/top_performer.csv'


def clearOverviewConnections(self):
    OverviewConnections.objects.filter(
        roomGroupName=self.room_group_name).delete()
    state_csv = pd.read_csv(STATE_CSV_PATH)
    state_csv = state_csv[state_csv['roomGroupName'] != self.room_group_name]
    state_csv.to_csv(STATE_CSV_PATH, index=False)

def clearProfileConnections(self):
    ProfileConnections.objects.filter(
        roomGroupName=self.room_group_name).delete()
    state_csv = pd.read_csv(STATE_CSV_PATH)
    state_csv = state_csv[state_csv['roomGroupName'] != self.room_group_name]
    state_csv.to_csv(STATE_CSV_PATH, index=False)


def clearStateCSV(self):
    FUNCTION_NAME = 'clearStateCSV'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    clearOverviewConnections(self)
    clearProfileConnections(self)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run(self):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    print(self)
    clearStateCSV(self)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
