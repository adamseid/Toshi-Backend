
import pandas as pd
from datetime import datetime
from requests import get
from web3 import Web3
from Historic_Crypto import HistoricalData, Cryptocurrencies
from datetime import datetime
import time
import os

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


def run(walletAddress):
    wallet_address = walletAddress
    getAssets(wallet_address)


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

def getAssets(wallet_address):
    # AssetTable.objects.all().delete()
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
        # asset_table = AssetTable(tokenName=tokenName, tokenAbbreviation=tokenAbbreviation, AmountInEth = AmountInEth, tokenAllocation = tokenAllocation, AmountInEthUSD = AmountInEthUSD,changeInTokenPrice = changeInTokenPrice)
        # asset_table.save()
        