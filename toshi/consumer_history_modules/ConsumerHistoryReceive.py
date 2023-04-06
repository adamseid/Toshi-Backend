from . import Misc
from ..models import HistoryConnections
from .receive import HistoryV3, HistoryV4

FILE_NAME = 'Receive'
DEBUG = True


def run(self, data):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    if data['request'] == "connect":
        room_group_name = self.room_group_name
        walletAddress = data['walletAddress']
        addConnectionToDatabase(room_group_name,walletAddress)
        HistoryPageData(self, data)

    print("ON RECIEVE END: ", self.room_group_name)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

def HistoryPageData(self, data):
    return HistoryV4.run(self, data)
    # return HistoryV3.run(self, data)

def addConnectionToDatabase(room_group_name,walletAddress ):
    conn = HistoryConnections(
        walletID=walletAddress,
        roomGroupName=room_group_name,
    )
    conn.save()
