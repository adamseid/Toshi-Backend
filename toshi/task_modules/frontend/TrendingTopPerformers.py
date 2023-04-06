from . import Misc
import pandas as pd
from syncer import sync
import time
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from ...models import TrendingTopPerformers
from datetime import datetime

FILE_NAME = 'TrendingTopPerformers'
DEBUG = True

unix_hour = 3600
unix_day = 86400
unix_week = 604800
unix_month = 2628000


def getCurrentCSV():
    return pd.DataFrame(list(TrendingTopPerformers.objects.all().values()))


@sync
async def sendTrendingTopPerformers(room_group_name, time_frame, current_csv):
    FUNCTION_NAME = 'sendTrendingTopPerformers'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    trendingTopPerformers = []
    for index, items in current_csv.iterrows():
        tempItem = [
            items['walletAddress'],
            items['Asset'],
            items['growth1H'],
            items['growth1D'],
            items['growth1W'],
            items['growth1M'],
            items['growth1Y'],
            items['growthChange1H'],
            items['growthChange1D'],
            items['growthChange1W'],
            items['growthChange1M'],
            items['growthChange1Y'],
        ]
        trendingTopPerformers.append(tempItem)

    data = {
        'response': 'update-trending-table',
        'filtered_transactions':  list(trendingTopPerformers)
    }

    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        room_group_name, {
            'type': "frontend.response",
            'data': str(data).replace("'", '"')
        }
    )

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run(state_csv):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    current_csv = getCurrentCSV()

    for i in range(len(state_csv)):

        if state_csv['timeFrame'][i] == 0 or state_csv['timeFrame'][i] == 'test':
            pass
        else:
            sendTrendingTopPerformers(state_csv['roomGroupName'][i],
                                      state_csv['timeFrame'][i], current_csv)

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
