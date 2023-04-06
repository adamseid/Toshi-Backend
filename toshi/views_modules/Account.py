from ..views_modules import Misc
from requests import get
from requests import get
from datetime import datetime
from channels.layers import get_channel_layer
from Historic_Crypto import LiveCryptoData
from web3 import Web3
import yfinance as yf
import time
import pandas as pd
from syncer import sync


FILE_NAME = 'AccountOverview'
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



def run(walletAddress):
    FUNCTION_NAME = 'run'

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    accountData = generateGraph(walletAddress)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
    return accountData

def get_account_balance(wallet_address):
    balance_url = make_api_url(
        "account", "balance", wallet_address, tag="latest")
    response = get(balance_url)

    data = response.json()
    value = int(data["result"]) / ETHER_VALUE
    return value


def generateGraph(nonCheckSumWalletAddress):

    custom_unix = unix_year
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    
    walletAddress = Web3.toChecksumAddress('0x' + str(nonCheckSumWalletAddress[-40:]))

    blockNumber = get_block_number(walletAddress,custom_unix)
    graphData = get_transactions(walletAddress,blockNumber,currentDateAndTime)
    walletBalance = round(get_account_balance(walletAddress),2)
    graphData.append(walletBalance)
    return graphData

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
def get_transactions(wallet_address, blockNumber,currentTime):

    current_balance = 0
    price_difference = 0
    balanceArray = []
    hourly_filtered_object_balance = []
    daily_filtered_object_balance = []
    weekly_filtered_object_balance = []
    monthly_filtered_object_balance = []
    yearly_filtered_object_balance = []
    price_difference_percentage = 0

    last_hour = int(currentTime - unix_hour)
    last_day = int(currentTime - unix_day)
    last_week = int(currentTime - unix_week)
    last_month = int(currentTime - unix_month)

    new =  LiveCryptoData('ETH-USD', verbose = False).return_data()

    transactions_url = make_api_url("account", "txlist", wallet_address,
                                    startblock=blockNumber, endblock=99999999, page=1, offset=2000, sort="desc")
    response = get(transactions_url)
    data = response.json()["result"]
    internal_tx_url = make_api_url("account", "txlistinternal", wallet_address,
                                   startblock=blockNumber, endblock=99999999, page=1, offset=2000, sort="desc")
    response2 = get(internal_tx_url)
    data2 = response2.json()["result"]
    data.extend(data2)
    data.sort(key=lambda x: int(x['timeStamp']))
    if(len(data) == 0):
        return [0,0,0,0]
    profit = 0
    profitable_transactions = 0
    non_profitable_transactions = 0

    for idx, tx in enumerate(data):
        to = tx["to"]
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
        
        balanceArray.append(current_balance)
        
        yearly_filtered_object_balance.append({
            "amt" : (int(time)),
            "pv": int(current_balance)
        })

        if(idx > 0):
            diff = value - yearly_filtered_object_balance[idx-1]['pv']
            profit = profit + diff
            if(profit > 0):
                profitable_transactions = profitable_transactions + 1
            else:
                non_profitable_transactions = non_profitable_transactions + 1

        integerTime = int(time)
        if integerTime > last_hour:    
            hourly_filtered_object_balance.append({
                "amt" : (int(time)),
                "pv": int(current_balance)
            })
        if integerTime > last_day:    
            daily_filtered_object_balance.append({
                "amt" : (int(time)),
                "pv": int(current_balance)
            })
        if integerTime > last_week:    
            weekly_filtered_object_balance.append({
                "amt" : (int(time)),
                "pv": int(current_balance)
            })
        if integerTime > last_month:    
            monthly_filtered_object_balance.append({
                "amt" : (int(time)),
                "pv": int(current_balance)
            })

    ticker = "ETH-USD"
    Token_Ticker = yf.Ticker(ticker)
    TOKEN_Data = Token_Ticker.history(period="1d")
    TOKEN_Data_Open = TOKEN_Data['Open']
    profit = profit/float(TOKEN_Data_Open)

    return[round(profit*-1,2), profitable_transactions + non_profitable_transactions, profitable_transactions, round((profitable_transactions/(profitable_transactions + non_profitable_transactions))*100)]

