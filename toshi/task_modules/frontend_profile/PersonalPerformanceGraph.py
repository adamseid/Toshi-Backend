from ..frontend_profile import Misc
from requests import get
from requests import get
from ...models import ProfileConnections
from datetime import datetime
from channels.layers import get_channel_layer
from Historic_Crypto import LiveCryptoData
from web3 import Web3

import time
import pandas as pd
from syncer import sync


FILE_NAME = 'PersonalPerformanceGraph'
DEBUG = True
API_KEY = "239PUCE9PMQCURRRZPVXRBESYPF4HUHRMZ"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18
ALCHEMY_API = "_mEa4ksrzCdb8fgB5_7-4doIZrMWwpKf"
ETHPLORER_API = "EK-joHSG-JyCU9Ay-jsqCh"

unix_hour = 3600
unix_day = 86400
unix_week = 604800
unix_month = 2628000
unix_year = 31540000



def run(state_csv):
    FUNCTION_NAME = 'run'

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    for i in range(len(state_csv)):

        if state_csv['timeFrame'][i] == 0 or state_csv['timeFrame'][i] == 'test':
            pass
        else:
            generateGraph(state_csv['roomGroupName'][i],
                      state_csv['timeFrame'][i], state_csv)

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

@sync
async def generateGraph(group_name, time_frame, data):

    custom_unix = 0
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    tempWalletAddress = ""
    for index, row in data.iterrows():
        if(row['walletID'] != ""):
            tempWalletAddress = row['walletID'].replace('"', '')
            
    walletAddress = Web3.toChecksumAddress('0x' + str(tempWalletAddress[-40:]))
    print("WALLET ADDRESS")
    print(walletAddress)
    if time_frame == '1H':
        custom_unix = unix_hour
    elif time_frame == '1D':
        custom_unix = unix_day
    elif time_frame == '1W':
        custom_unix = unix_week
    elif time_frame == '1M':
        custom_unix = unix_month
    else:
        custom_unix = unix_year
    new =  LiveCryptoData('ETH-USD', verbose = False).return_data()
    blockNumber = get_block_number(walletAddress,custom_unix)
    graphData = get_transactions(walletAddress,blockNumber)
    account_balance = get_account_balance(walletAddress)*int(float(new['ask'][0]))
    graphData.append(account_balance)
    data = {
        'response': 'update-graph',
        'data':  list(graphData)
    }

    channel_layer = get_channel_layer()

    await channel_layer.group_send(
        group_name, {
            'type': "profilefrontend.response",
            'data': str(data).replace("'", '"')
        }
    )



def get_account_balance(wallet_address):
    balance_url = make_api_url(
        "account", "balance", wallet_address, tag="latest")
    response = get(balance_url)

    data = response.json()
    value = int(data["result"]) / ETHER_VALUE
    return value


def make_api_url(module, action, wallet_address, **kwargs):
    url = BASE_URL + \
        f"?module={module}&action={action}&address={wallet_address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url

def get_block_number(wallet_address,custom_unix):
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    last_year_unix = int(currentDateAndTime - custom_unix)
    block_url = make_api_url(module="block", action="getblocknobytime",
                             wallet_address=wallet_address, closest="before", timestamp=last_year_unix)
    response = get(block_url)
    data = response.json()
    value = int(data["result"])
    return value

# GETS A LIST OF ALL TRANSACTIONS SEPREATED BY 2 COLUMNS. (TIME, WALLET BALANCE AT THAT TIME)
def get_transactions(wallet_address, blockNumber):
    # TopPerformanceGraph.objects.all().delete()
    new =  LiveCryptoData('ETH-USD', verbose = False).return_data()
    transactions_url = make_api_url("account", "txlist", wallet_address,
                                    startblock=blockNumber, endblock=99999999, page=1, offset=10000, sort="desc")
    response = get(transactions_url)
    data = response.json()["result"]
    internal_tx_url = make_api_url("account", "txlistinternal", wallet_address,
                                   startblock=blockNumber, endblock=99999999, page=1, offset=10000, sort="desc")
    response2 = get(internal_tx_url)
    data2 = response2.json()["result"]
    data.extend(data2)
    data.sort(key=lambda x: int(x['timeStamp']))
    current_balance = 0
    dataTransactions = []
    timeArray = []
    price_difference = 0
    balanceArray = []
    filtered_object_balance = []
    price_difference_percentage = 0
    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / ETHER_VALUE
        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETHER_VALUE
        time = str(tx['timeStamp'])
        money_in = to.lower() == wallet_address.lower()
        if money_in:
            current_balance += value
        else:
            current_balance -= value + gas
        timeArray.append(time)
        balanceArray.append(current_balance)
        filtered_object_balance.append({
                    "amt" : (int(time)),
                    "pv": int(current_balance*int(float(new['ask'][0])))
                })
    if len(balanceArray)> 0:
        price_difference = balanceArray[0]*int(float(new['ask'][0])) - balanceArray[-1]*int(float(new['ask'][0]))
        price_difference_percentage = price_difference/(balanceArray[0]*int(float(new['ask'][0])))
    return [filtered_object_balance,price_difference,price_difference_percentage]
