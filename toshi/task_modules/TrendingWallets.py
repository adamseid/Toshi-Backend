
from .trending_wallets import Misc
import pandas as pd
from datetime import datetime
import time
from requests import get
from ..models import TopPerformanceGraph,AssetTable, TrendingTopPerformers
from web3 import Web3
import requests
from Historic_Crypto import HistoricalData, Cryptocurrencies

FILE_NAME = 'TrendingWallets'
DEBUG = True

ALCHEMY_API = "_mEa4ksrzCdb8fgB5_7-4doIZrMWwpKf"
ETHPLORER_API = "EK-joHSG-JyCU9Ay-jsqCh"
API_KEY = "239PUCE9PMQCURRRZPVXRBESYPF4HUHRMZ"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18
unix_hour = 3600
unix_day = 86400
unix_week = 604800
unix_month = 2628000
unix_year = 31540000

def update():
    FUNCTION_NAME = 'update'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/81864056f2f746488fcfd136ee6cc122"))
    blockNumber = web3.eth.blockNumber - 1
    block = web3.eth.getBlock(blockNumber)
    wallet_address = block["transactions"][0].hex()

    transactionsListUrl = "https://blockscout.com/eth/mainnet/api?module=account&action=txlist&address=" + "0xa542f325990CEB47e2AE8BD9dccF8960b16eB7a9" 
    response = get(transactionsListUrl)
    data = response.json()
    transactions = data['result']
    if len(transactions) > 1 and not TrendingTopPerformers.objects.filter(walletAddress=wallet_address).exists():
        top_asset = getTopAssets(wallet_address)
        block_number = get_block_number(wallet_address)
        transaction_data = get_transactions(wallet_address, block_number)
        transactionsArray = splitTransactions(transaction_data)
        hourly_transaction = transactionsArray[0]
        daily_transaction = transactionsArray[1]
        weekly_transaction = transactionsArray[2]
        monthly_transaction = transactionsArray[3]
        yearly_transaction = transaction_data
        hourly_change = 0
        daily_change = 0
        weekly_change = 0
        monthly_change = 0
        yearly_change = 0
        hourly_change_percentage = 0
        daily_change_percentage = 0
        weekly_change_percentage = 0
        monthly_change_percentage = 0
        yearly_change_percentage = 0

        if len(hourly_transaction) > 2:
            hourly_change = hourly_transaction[-1][1] - hourly_transaction[0][1]
            hourly_change_percentage = round((hourly_change/hourly_transaction[0][1])*100,2)

        if len(daily_transaction) > 2:
            daily_change = daily_transaction[-1][1] - daily_transaction[0][1]
            daily_change_percentage = round((daily_change/daily_transaction[0][1])*100,2)

        if len(weekly_transaction) > 2:
            weekly_change = weekly_transaction[-1][1] - weekly_transaction[0][1]
            weekly_change_percentage = round((weekly_change/weekly_transaction[0][1])*100,2)

        if len(monthly_transaction) > 2:
            monthly_change = monthly_transaction[-1][1] - monthly_transaction[0][1]
            monthly_change_percentage = round((monthly_change/monthly_transaction[0][1])*100,2)

        if len(yearly_transaction) > 2:
            yearly_change = yearly_transaction[-1][1] - yearly_transaction[0][1]
            yearly_change_percentage = round((yearly_change/yearly_transaction[0][1])*100,2)

        trendingTopPerformers = TrendingTopPerformers(
            walletAddress= wallet_address, 
            Asset=top_asset, 
            growth1H = hourly_change,
            growth1D = daily_change,
            growth1W = weekly_change,
            growth1M = monthly_change,
            growth1Y = yearly_change,
            growthChange1H = hourly_change_percentage,
            growthChange1D = daily_change_percentage,
            growthChange1W = weekly_change_percentage,
            growthChange1M = monthly_change_percentage,
            growthChange1Y = yearly_change_percentage
        )
        trendingTopPerformers.save()
    else:
        print("USER ALREADY EXISTS")


    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

def getlastDatePrice(tokenSymbol):
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    yesterday_first = currentDateAndTime - unix_day - unix_hour
    yesterday_second = currentDateAndTime - unix_day
    date_first = datetime.fromtimestamp(yesterday_first).strftime("%Y") + "-" + datetime.fromtimestamp(yesterday_first).strftime("%m") + "-" + datetime.fromtimestamp(yesterday_first).strftime("%d") + "-" + datetime.fromtimestamp(yesterday_first).strftime("%H") + "-" + datetime.fromtimestamp(yesterday_first).strftime("%M") 
    date_second = datetime.fromtimestamp(yesterday_second).strftime("%Y") + "-" + datetime.fromtimestamp(yesterday_second).strftime("%m") + "-" + datetime.fromtimestamp(yesterday_second).strftime("%d") + "-" + datetime.fromtimestamp(yesterday_second).strftime("%H") + "-" + datetime.fromtimestamp(yesterday_second).strftime("%M")
    
    data = Cryptocurrencies(coin_search = tokenSymbol, extended_output=False).find_crypto_pairs()
    if tokenSymbol in data['display_name'].iloc[0]:
        price_symbol = tokenSymbol + '-USD'
        old = int(HistoricalData(price_symbol,300, str(date_first),str(date_second)).retrieve_data()['low'].iloc[0])
    else:
        old = 0
    return old

def getTopAssets(wallet_address):
    alchemy_url = "https://api.ethplorer.io/getAddressInfo/" + wallet_address + "?apiKey=freekey" 
    response = get(alchemy_url)
    data = response.json()
    tokenInfo = data['tokens']
    pair = [-1.0,"tokenName"]

    for tokens in tokenInfo:
        tokenAbbreviation = tokens['tokenInfo']['symbol']
        AmountInEth = (tokens["balance"] / ETHER_VALUE)
        AmountInEthUSD = tokens['tokenInfo']['price']['rate'] * AmountInEth
        if AmountInEthUSD >= pair[0]:
            pair[0] = int(AmountInEthUSD)
            pair[1] = tokenAbbreviation
    return pair[1]
    


def getAssets(wallet_address):
    AssetTable.objects.all().delete()
    alchemy_url = "https://api.ethplorer.io/getAddressInfo/" + wallet_address + "?apiKey=freekey"
    response = get(alchemy_url)
    data = response.json()
    tokenInfo = data['tokens']
    tokenSum = 0
    for tokens in tokenInfo:
        tokenSum = tokenSum + (tokens["balance"] / ETHER_VALUE)

    for tokens in tokenInfo:
        tokenName = tokens['tokenInfo']['name']
        tokenAbbreviation = tokens['tokenInfo']['symbol']
        AmountInEth = (tokens["balance"] / ETHER_VALUE)
        tokenAllocation = AmountInEth / tokenSum
        AmountInEthUSD = tokens['tokenInfo']['price']['rate'] * AmountInEth
        initialTokenPrice = getlastDatePrice(tokenAbbreviation) * AmountInEth
        if initialTokenPrice == 0:
            changeInTokenPrice = 0
        else:
            changeInTokenPrice = (AmountInEthUSD - initialTokenPrice)/ initialTokenPrice
        asset_table = AssetTable(tokenName=tokenName, tokenAbbreviation=tokenAbbreviation, AmountInEth = AmountInEth, tokenAllocation = tokenAllocation, AmountInEthUSD = AmountInEthUSD,changeInTokenPrice = changeInTokenPrice)
        asset_table.save()
        



def splitTransactions(transaction_data):
    currentDateAndTime = time.mktime(datetime.now().timetuple())

    last_hour_unix = int(currentDateAndTime - unix_hour)
    last_daily_unix = int(currentDateAndTime - unix_day)
    last_weekly_unix = int(currentDateAndTime - unix_week)
    last_monthly_unix = int(currentDateAndTime - unix_month)

    hour_transactions = []
    daily_transactions = []
    weekly_transactions = []
    monthly_transactions = []

    for data in transaction_data:
        if data[0] >= last_hour_unix:
            hour_transactions.append(data)
        if data[0] >= last_daily_unix:
            daily_transactions.append(data)
        if data[0] >= last_weekly_unix:
            weekly_transactions.append(data)
        if data[0] >= last_monthly_unix:
            monthly_transactions.append(data)

    return (hour_transactions, daily_transactions, weekly_transactions, monthly_transactions)


def make_api_url(module, action, wallet_address, **kwargs):
    url = BASE_URL + \
        f"?module={module}&action={action}&address={wallet_address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url

# GETS A LIST OF ALL TRANSACTIONS SEPREATED BY 2 COLUMNS. (TIME, WALLET BALANCE AT THAT TIME)
def get_block_number(wallet_address):
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    last_year_unix = int(currentDateAndTime - unix_year)
    block_url = make_api_url(module="block", action="getblocknobytime",
                             wallet_address=wallet_address, closest="before", timestamp=last_year_unix)
    response = get(block_url)
    data = response.json()
    value = int(data["result"])
    return value

# GETS A LIST OF ALL TRANSACTIONS SEPREATED BY 2 COLUMNS. (TIME, WALLET BALANCE AT THAT TIME)
def get_transactions(wallet_address, blockNumber):
    TopPerformanceGraph.objects.all().delete()
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
    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / ETHER_VALUE
        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETHER_VALUE
        # time = datetime.fromtimestamp(int(tx['timeStamp']))
        time = int(tx['timeStamp'])
        money_in = to.lower() == wallet_address.lower()
        if money_in:
            current_balance += value
        else:
            current_balance -= value + gas
        pair = (time, current_balance)
        dataTransactions.append(pair)
        # tpwp = TopPerformanceGraph(time=time, balance=current_balance)
        # tpwp.save()
    return dataTransactions
