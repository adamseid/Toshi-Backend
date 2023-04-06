from ... import Misc
from .header import PersonalAssetsTable,PersonalPerformanceGraph
import os
from ....models import ProfileConnections


FILE_NAME = 'Header'
DEBUG = True


def run(self, data):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    walletAddress = data['time_frame']
    if(walletAddress != ""):
        pc = ProfileConnections(roomGroupName = self.room_group_name, walletID = data['time_frame'] )
        pc.save()
        
    
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
