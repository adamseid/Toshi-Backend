from . import Misc
import pandas as pd
from syncer import sync
import time
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from ...models import DailyTopPerformers, OverviewConnections
from datetime import datetime

FILE_NAME = 'Daily Top Performers'
DEBUG = True

unix_hour = 3600
unix_day = 86400
unix_week = 604800
unix_month = 2628000


def getCurrentCSV():
    return pd.DataFrame(list(DailyTopPerformers.objects.all().values()))

@sync
async def sendDailyTopPerformer(room_group_name, time_frame, current_csv, x):
    state_csv = x
    FUNCTION_NAME = 'sendDailyTopPerformer'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    idx = 0
    for i in range(len(state_csv)):
        if state_csv['roomGroupName'][i] == room_group_name:
            idx = int(i)
    dailyTopPerformers = []
    for index, items in current_csv.iterrows():
        if state_csv['timeFrameTable'][idx] == "1H":
            tempItem = [
                items['walletAddress'],
                items['Asset'],
                items['growth1H'],
                items['growthChange1H']
            ]
        if state_csv['timeFrameTable'][idx] == "1D":
            tempItem = [
                items['walletAddress'],
                items['Asset'],
                items['growth1D'],
                items['growthChange1D'],
            ]
        if state_csv['timeFrameTable'][idx] == "1W":
            tempItem = [
                items['walletAddress'],
                items['Asset'],
                items['growth1W'],
                items['growthChange1W'],
            ]
        if state_csv['timeFrameTable'][idx] == "1M":
            tempItem = [
                items['walletAddress'],
                items['Asset'],
                items['growth1M'],
                items['growthChange1M'],
            ]
        if state_csv['timeFrameTable'][idx] == "1Y":
            tempItem = [
                items['walletAddress'],
                items['Asset'],
                items['growth1Y'],
                items['growthChange1Y'],
            ]
        dailyTopPerformers.append(tempItem)
    data = {
        'response': 'update-daily-top-performers',
        'filtered_transactions':  list(dailyTopPerformers)
    }

    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        room_group_name, {
            'type': "frontend.response",
            'data': str(data).replace("'", '"')
        }
    )

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run(x):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    state_csv = pd.DataFrame(
        list(OverviewConnections.objects.all().values()))
    current_csv = getCurrentCSV()

    for i in range(len(state_csv)):

        if state_csv['timeFrame'][i] == 0 or state_csv['roomGroupName'][i] == 'test':
            pass
        else:
            sendDailyTopPerformer(state_csv['roomGroupName'][i],
                                  state_csv['timeFrameTable'][i], current_csv, x)

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
