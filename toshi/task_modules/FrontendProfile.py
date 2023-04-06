from .frontend_profile import AssetTable, PersonalPerformanceGraph, Misc
import pandas as pd
from ..models import ProfileConnections


FILE_NAME = 'Frontend'
DEBUG = True
STATE_CSV_PATH = './toshi/state/top_performer.csv'


def update():
    FUNCTION_NAME = 'update'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    state_csv = pd.DataFrame(list(ProfileConnections.objects.all().values()))
    print(state_csv)

    # if len(state_csv) == 0:
    #     pass
    # else:
    #     PersonalPerformanceGraph.run(state_csv)
    #     AssetTable.run(state_csv)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
