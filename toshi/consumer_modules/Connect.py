from . import Misc
from .receive import Select
from ..models import OverviewConnections


FILE_NAME = 'Connect'
DEBUG = True


def run(self):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    room_group_name = self.room_group_name
    print(room_group_name)
    oc = OverviewConnections(
        roomGroupName=room_group_name, timeFrame="1Y", timeFrameTable="1Y")
    oc.save()
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
