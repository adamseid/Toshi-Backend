from .frontend import Misc
from .frontend import Graph, DailyTopPerformers, TrendingTopPerformers
import pandas as pd
from ..models import OverviewConnections


FILE_NAME = 'Frontend'
DEBUG = True
STATE_CSV_PATH = './toshi/state/top_performer.csv'


def update():
    FUNCTION_NAME = 'update'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    state_csv = pd.DataFrame(
        list(OverviewConnections.objects.all().values()))

    if len(state_csv) == 0:
        pass
    else:
        Graph.run(state_csv)
        DailyTopPerformers.run(state_csv)
        TrendingTopPerformers.run(state_csv)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
