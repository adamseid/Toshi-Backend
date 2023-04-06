from . import Misc
import pandas as pd
from syncer import sync
import time
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from ...models import TopPerformanceGraph, DailyTopPerformers
from datetime import datetime
from Historic_Crypto import LiveCryptoData


FILE_NAME = 'Graph'
DEBUG = True

unix_hour = 3600
unix_day = 86400
unix_week = 604800
unix_month = 2628000


def getCurrentCSV():
    return pd.DataFrame(list(TopPerformanceGraph.objects.all().values()))

@sync
async def sendGraph(room_group_name, time_frame, current_csv):
    FUNCTION_NAME = 'sendGraph'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    # current_csv = pd.DataFrame()  # getCurrentCSV()
    new =  LiveCryptoData('ETH-USD', verbose = False).return_data()
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    last_hourly_unix = int(currentDateAndTime - unix_hour)
    last_daily_unix = int(currentDateAndTime - unix_day)
    last_weekly_unix = int(currentDateAndTime - unix_week)
    last_monthly_unix = int(currentDateAndTime - unix_month)

    filtered_time = []
    filtered_balance = []
    filtered_object_balance = []
    price_difference = 0



    for index, row in current_csv.iterrows():
        time_name = coinGeckounixTimeStampToDateTime(row['time'])

        if time_frame == '1H':
            if int(row['time']) >= last_hourly_unix:
                filtered_time.append(int(row['time']))
                filtered_balance.append(int(row['balance']))
                filtered_balance.append(int(row['balance']))
                filtered_object_balance.append({
                    "time" : (int(row['time'])),
                    "USD": int(row['balance']*int(float(new['ask'][0]))),
                    "time_name": time_name
                })

        if time_frame == '1D':
            if int(row['time']) >= last_daily_unix:
                filtered_time.append(int(row['time']))
                filtered_balance.append(int(row['balance']))
                filtered_balance.append(int(row['balance']))
                filtered_object_balance.append({
                    "time" : (int(row['time'])),
                    "USD": int(row['balance']*int(float(new['ask'][0]))),
                    "time_name": time_name
                })

        if time_frame == '1W':
            if int(row['time']) >= last_weekly_unix:
                filtered_time.append(int(row['time']))
                filtered_balance.append(int(row['balance']))
                filtered_balance.append(int(row['balance']))
                filtered_object_balance.append({
                    "time" : (int(row['time'])),
                    "USD": int(row['balance']*int(float(new['ask'][0]))),
                    "time_name": time_name
                })

        if time_frame == '1M':
            if int(row['time']) >= last_monthly_unix:
                filtered_time.append(int(row['time']))
                filtered_balance.append(int(row['balance']))
                filtered_balance.append(int(row['balance']))
                filtered_object_balance.append({
                    "time" : (int(row['time'])),
                    "USD": int(row['balance']*int(float(new['ask'][0]))),
                    "time_name": time_name
                })

        if time_frame == '1Y':
            filtered_time.append(int(row['time']))
            filtered_balance.append(int(row['balance']))
            filtered_balance.append(int(row['balance']))
            filtered_object_balance.append({
                "time" : (int(row['time'])),
                "USD": int(row['balance']*int(float(new['ask'][0]))),
                "time_name": time_name
            })
    if len(filtered_balance)> 0:
        price_difference = filtered_balance[0]*int(float(new['ask'][0])) - filtered_balance[-1]*int(float(new['ask'][0]))
    filtered_transactions = ([filtered_object_balance, price_difference])
    data = {
        'response': 'update-graph',
        'filtered_transactions':  list(filtered_transactions)
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
            sendGraph(state_csv['roomGroupName'][i],
                      state_csv['timeFrame'][i], current_csv)

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def coinGeckounixTimeStampToDateTime(unix):
    return (
        datetime.fromtimestamp(
            int(unix)
        ).strftime('%d-%m-%Y')
    )