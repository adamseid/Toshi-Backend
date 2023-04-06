from ..views_modules import Misc
from requests import get
import time
from ..models import historic, contracts, coinList
import sys
from datetime import datetime
from channels.layers import get_channel_layer
from Historic_Crypto import LiveCryptoData
from web3 import Web3
import yfinance as yf
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor


import time
import pandas as pd
from syncer import sync


FILE_NAME = 'AccountDetailed'
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
    # coins = getListOfCrypto()
    # for items in coins:
    #     coins = coinList(
    #         identification=items['id'],
    #         symbol=items['symbol'],
    #         name=items['name']
    #     )
    #     coins.save()
    accountData = generateDetailedAssets(walletAddress)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
    return accountData


def generateDetailedAssets(nonCheckSumWalletAddress):

    custom_unix = unix_year
    walletAddress = Web3.toChecksumAddress(
        '0x' + str(nonCheckSumWalletAddress[-40:]))

    blockNumber = get_block_number(walletAddress, custom_unix)
    graphData = get_transactions(
        walletAddress, blockNumber)
    return graphData


def make_api_url(module, action, wallet_address, **kwargs):
    url = BASE_URL + \
        f"?module={module}&action={action}&address={wallet_address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url


def get_block_number(wallet_address, custom_unix):
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    last_year_unix = int(currentDateAndTime - custom_unix)
    block_url = make_api_url(module="block", action="getblocknobytime",
                             wallet_address=wallet_address, closest="before", timestamp=last_year_unix)
    response = get(block_url)
    data = response.json()
    value = int(data["result"])
    return value


def unixTimeStampToDateTime(unix):
    return (
        datetime.fromtimestamp(
            int(unix)
        ).strftime('%Y-%m-%d')
    )

def coinGeckounixTimeStampToDateTime(unix):
    return (
        datetime.fromtimestamp(
            int(unix)
        ).strftime('%d-%m-%Y')
    )

def get_transactions(wallet_address, blockNumber):
    transactions_url = make_api_url(
        "account",
        "tokentx",
        wallet_address,
        startblock=0,
        endblock=99999999,
        page=1,
        offset=10000,
        sort="asc"
    )
    response = get(transactions_url)
    data = response.json()["result"]

    normal_transactions_url = make_api_url("account", "txlist", wallet_address,
                                           startblock=0, endblock=99999999, page=1, offset=2000, sort="desc")
    normal_response = get(normal_transactions_url)
    normal_data = normal_response.json()["result"]
    normal_data.sort(key=lambda x: int(x['timeStamp']))

    return handleTransactions(wallet_address, data, normal_data)


def token(tx):
    if not historic.objects.filter(token=tx['tokenSymbol'], date=int(tx['timeStamp'])).exists():
        ticker = tx['tokenSymbol'] + "-ETH"
        Token_Ticker = yf.Ticker(ticker)
        startTime = unixTimeStampToDateTime(int(tx['timeStamp']) - 86400)
        endTime = unixTimeStampToDateTime(int(tx['timeStamp']))
        try:
            TOKEN_Data = Token_Ticker.history(start=startTime, end=endTime)
            return [True, TOKEN_Data, tx]
        except Exception as e:
            return [False, 0, tx]
    return [False, 0, tx]

def getListOfCrypto():
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=false"
    response = get(url)
    data = response.json()
    return data

def getPastPriceCrypto(identification, date):
    url = "https://pro-api.coingecko.com/api/v3/coins/" + identification + "/history?date=" + date + "&localization=false" + "&x_cg_pro_api_key=CG-o8B8B9FoSYrQEDAoFeGveNZU"
    response = get(url)
    data = response.json()
    return data


def get_account_balance(wallet_address):
    balance_url = make_api_url(
        "account", "balance", wallet_address, tag="latest")
    response = get(balance_url)

    data = response.json()
    value = int(data["result"]) / ETHER_VALUE
    return value

def getTokenImages(tokenName):
    try: 
        # coin = coinList.objects.get(name=tokenName.lower())
        # id = coin.identification
        url = "https://api.coingecko.com/api/v3/coins/" + tokenName.lower().replace(" ", "-") + "?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"
        response = get(url)
        data = response.json()
        imageUrl = data["image"]["thumb"]
    except: 
        try:
            url = "https://api.coingecko.com/api/v3/coins/" + tokenName.lower().split()[0] + "?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"
            response = get(url)
            data = response.json()
            imageUrl = data["image"]["thumb"]
        except:
            imageUrl = ""
    return imageUrl


def individualTransaction(tx, wallet_address, balance, TOKEN_VALUE, ETH_VALUE):
    skip = False
    if contracts.objects.filter(contractAddress=tx['from']).exists() or contracts.objects.filter(contractAddress=tx['to']).exists():
        skip = True
    else:
        toAddress =  Web3.toChecksumAddress('0x' + str(tx['from'][-40:]))
        fromAddress =  Web3.toChecksumAddress('0x' + str(tx['to'][-40:]))
        web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/21a13d88d64f420d91ff5c3272c0f8b0"))
        toAddressHex = web3.eth.get_code(toAddress).hex()
        fromAddressHex = web3.eth.get_code(fromAddress).hex()
        if (toAddressHex == "0x" and fromAddressHex == "0x"):
            skip = False
        else:
            skip = True
            if (fromAddressHex == "0x"):
                contractsDatabase = contracts(contractAddress=tx['to'])
                contractsDatabase.save()
            elif (toAddressHex == "0x"):
                contractsDatabase = contracts(contractAddress=tx['from'])
                contractsDatabase.save()
    if(skip):
        if (tx['to'] == wallet_address.lower()):
            # MONEY IN
            if (balance.get(tx['tokenName'])):
                balance.update({
                    tx['tokenName']: [
                        balance.get(tx['tokenName'])[0] + 1,  # Total Transactions
                        balance.get(tx['tokenName'])[1],  # Profit Transactions
                        (balance.get(tx['tokenName'])[2] + \
                        (ETH_VALUE)),  # Profit Total
                        tx['tokenName'],  # Token Name
                        tx['tokenSymbol'],  # Token Acronym
                        # Asset Allocation
                        (TOKEN_VALUE + balance.get(tx['tokenName'])[5]),
                        0,  # Asset Allocation Percentage,
                        tx['contractAddress'],
                        (balance.get(tx['tokenName'])[8] + \
                        (ETH_VALUE)), # Total Money In
                        balance.get(tx['tokenName'])[9], # Money out
                        balance.get(tx['tokenName'])[10],
                        balance.get(tx['tokenName'])[11]
                    ]
                })
            else:
                image = getTokenImages(tx['tokenName'])
                balance.update({
                    tx['tokenName']: [
                        1,  # Total Transactions
                        0,  # Profit Transactions
                        ETH_VALUE,  # Profit Total
                        tx['tokenName'],  # Token Name
                        tx['tokenSymbol'],  # Token Acronym
                        TOKEN_VALUE,  # Asset Allocation
                        0,  # Asset Allocation Percentage
                        tx['contractAddress'],
                        ETH_VALUE, # Total Money In
                        0, # Money out
                        0, # total gas price
                        image # token image
                    ]
                })
        else:
            # MONEY OUT
            if (balance.get(tx['tokenName'])):
                balance.update({
                    tx['tokenName']: [
                        balance.get(tx['tokenName'])[0] + 1,  # Total Transactions
                        balance.get(tx['tokenName'])[1] + 1,  # Profit Transactions
                        (balance.get(tx['tokenName'])[2] -(ETH_VALUE) - (float(tx['gasPrice'])/float(ETHER_VALUE))),  # Profit Total
                        tx['tokenName'],  # Token Name
                        tx['tokenSymbol'],  # Token Acronym
                        # Asset Allocation
                        (balance.get(tx['tokenName'])[5] - TOKEN_VALUE),
                        0,  # Asset Allocation Percentage
                        tx['contractAddress'],
                        balance.get(tx['tokenName'])[8],
                        (balance.get(tx['tokenName'])[9] -(ETH_VALUE) - (float(tx['gasPrice'])/float(ETHER_VALUE))), # Total Money Out
                        (balance.get(tx['tokenName'])[10] + (float(tx['gasPrice'])/float(ETHER_VALUE))),
                        balance.get(tx['tokenName'])[11]
                    ]
                })
            else:
                image = getTokenImages(tx['tokenName'])
                balance.update({
                    tx['tokenName']: [
                        1,  # Total Transactions
                        0,  # Profit Transactions
                        ETH_VALUE * -1.0 - (float(tx['gasPrice'])/float(ETHER_VALUE)),  # Profit Total
                        tx['tokenName'],  # Token Name
                        tx['tokenSymbol'],  # Token Acronym
                        0,  # Asset Allocation
                        0,  # Asset Allocation Percentage
                        tx['contractAddress'],
                        0, # Total Money In
                        ETH_VALUE * -1.0 - (float(tx['gasPrice'])/float(ETHER_VALUE)), # Total Money Out
                        (float(tx['gasPrice'])/float(ETHER_VALUE)),
                        image
                    ]
                })
    return balance


def handleTransactions(wallet_address, data, allTransactions):
    start_time = time.time()
    totalAssetsYearly = 0
    totalAssetsMonthly = 0
    totalAssetsWeekly = 0
    totalAssetsDaily = 0
    
    totalAssetsMax = 0
    # totalAssetsHourly = 0

    frontendDataMax = []
    frontendDataYearly = []
    frontendDataMonthly = []
    frontendDataWeekly = []
    frontendDataDaily = []
    # frontendDataHourly = []

    maxAssetBalance = dict()

    yearlyAssetBalance = dict()
    monthlyAssetBalance = dict()
    weeklyAssetBalance = dict()
    dailyAssetBalance = dict()
    # hourlyAssetBalance = dict()
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    monthlyTime = currentDateAndTime - unix_month
    weeklyTime = currentDateAndTime - unix_week
    # hourlyTime = currentDateAndTime - unix_hour
    dailyTime = currentDateAndTime - unix_day

    yearlyTime = currentDateAndTime - unix_year

    ETH_VALUE = 0
    transactionEthValue = dict()


    ticker = "ETH-USD"
    Token_Ticker = yf.Ticker(ticker)
    startTime = unixTimeStampToDateTime(int(dailyTime))
    endTime = unixTimeStampToDateTime(currentDateAndTime )

    TOKEN_Data = Token_Ticker.history(period="1d")
    TOKEN_Data_Open = TOKEN_Data['Open']
    TOKEN_Data_close = TOKEN_Data['Close']

    eth_price_change = float((TOKEN_Data_close - TOKEN_Data_Open)/(TOKEN_Data_Open))




    for trans in allTransactions:
        transactionEthValue.update({
            trans['hash']: int(trans['value'])/(10 ** 18)
        })

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(token, tx): tx for tx in data}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if (res[0]):
                USD = 0
                series = res[1]['Open']
                if (series.size > 0):
                    if (series.isnull().values.any()):
                        USD = 0
                    else:
                        USD = series[0]
                historicalCrypto = historic(
                    token=res[2]['tokenSymbol'],
                    date=res[2]['timeStamp'],
                    price=USD
                )
                historicalCrypto.save()
            else:
                historicalCrypto = historic(
                    token=res[2]['tokenSymbol'],
                    date=res[2]['timeStamp'],
                    price=0
                )
                historicalCrypto.save()

    for idx, tx in enumerate(data):
        if (coinList.objects.filter(symbol=tx['tokenSymbol'].lower())):
            TOKEN_VALUE = float(tx['value'])/(10 ** float(tx['tokenDecimal']))
            if tx['hash'] in transactionEthValue:
                ETH_VALUE = transactionEthValue[tx['hash']]
            else:
                date = coinGeckounixTimeStampToDateTime(tx['timeStamp'])
                ident = coinList.objects.filter(symbol=tx['tokenSymbol'].lower()).values()[0]['identification']
                pastPrice = getPastPriceCrypto(ident, date)
                if "market_data" in pastPrice:
                    ETH_VALUE = pastPrice['market_data']['current_price']['eth']
                else:
                    ETH_VALUE = historic.objects.filter(
                        token=tx['tokenSymbol'], date=tx['timeStamp']).values()[0]['price']
            maxAssetBalance = individualTransaction(tx, wallet_address, maxAssetBalance, TOKEN_VALUE, ETH_VALUE)
            
            if (int(tx['timeStamp']) > yearlyTime):
                yearlyAssetBalance = individualTransaction(
                    tx, wallet_address, yearlyAssetBalance, TOKEN_VALUE, ETH_VALUE)
            # yearlyAssetBalance = ass
            # if (int(tx['timeStamp']) > hourlyTime):
            #     hourlyAssetBalance = individualTransaction(
            #         tx, wallet_address, hourlyAssetBalance, TOKEN_VALUE, ETH_VALUE)
            if (int(tx['timeStamp']) > dailyTime):
                dailyAssetBalance = individualTransaction(
                    tx, wallet_address, dailyAssetBalance, TOKEN_VALUE, ETH_VALUE)
            if (int(tx['timeStamp']) > weeklyTime):
                weeklyAssetBalance = individualTransaction(
                    tx, wallet_address, weeklyAssetBalance, TOKEN_VALUE, ETH_VALUE)
            if (int(tx['timeStamp']) > monthlyTime):
                monthlyAssetBalance = individualTransaction(
                    tx, wallet_address, monthlyAssetBalance, TOKEN_VALUE, ETH_VALUE)

    walletBalance = get_account_balance(wallet_address)
    for x in maxAssetBalance:
        if (maxAssetBalance[x][5] > 0 and (maxAssetBalance[x][2] < walletBalance*10 or maxAssetBalance[x][2] <15)):
            maxAssetBalance[x][2] = round(maxAssetBalance[x][2], 4)
            maxAssetBalance[x][8] = round(maxAssetBalance[x][8], 4)
            maxAssetBalance[x][9] = abs(round(maxAssetBalance[x][9], 4))

            totalAssetsMax = totalAssetsMax + maxAssetBalance[x][5]
            maxAssetBalance[x][5] = round(maxAssetBalance[x][5])
            frontendDataMax.append(maxAssetBalance[x])
    for x in yearlyAssetBalance:
        if (yearlyAssetBalance[x][5] > 0 and (yearlyAssetBalance[x][2] < walletBalance*10 or yearlyAssetBalance[x][2] <15)):
            yearlyAssetBalance[x][2] = round(yearlyAssetBalance[x][2], 4)
            yearlyAssetBalance[x][8] = round(yearlyAssetBalance[x][8], 4)
            yearlyAssetBalance[x][9] = abs(round(yearlyAssetBalance[x][9], 4))

            totalAssetsYearly = totalAssetsYearly + yearlyAssetBalance[x][5]
            yearlyAssetBalance[x][5] = round(yearlyAssetBalance[x][5])
            frontendDataYearly.append(yearlyAssetBalance[x])
    for x in monthlyAssetBalance:
        if (monthlyAssetBalance[x][5] > 0 and (monthlyAssetBalance[x][2] < walletBalance*10 or monthlyAssetBalance[x][2] <15)):
            monthlyAssetBalance[x][2] = round(monthlyAssetBalance[x][2], 4)
            yearlyAssetBalance[x][8] = round(yearlyAssetBalance[x][8], 4)
            yearlyAssetBalance[x][9] = abs(round(yearlyAssetBalance[x][9], 4))

            totalAssetsMonthly = totalAssetsMonthly + monthlyAssetBalance[x][5]
            monthlyAssetBalance[x][5] = round(monthlyAssetBalance[x][5])
            frontendDataMonthly.append(monthlyAssetBalance[x])

    for x in weeklyAssetBalance:
        if (weeklyAssetBalance[x][5] > 0 and (weeklyAssetBalance[x][2] < walletBalance*10 or weeklyAssetBalance[x][2] <15)):
            weeklyAssetBalance[x][2] = round(weeklyAssetBalance[x][2], 4)
            yearlyAssetBalance[x][8] = round(yearlyAssetBalance[x][8], 4)
            yearlyAssetBalance[x][9] = abs(round(yearlyAssetBalance[x][9], 4))

            totalAssetsWeekly = totalAssetsWeekly + weeklyAssetBalance[x][5]
            weeklyAssetBalance[x][5] = round(weeklyAssetBalance[x][5])
            frontendDataWeekly.append(weeklyAssetBalance[x])

    for x in dailyAssetBalance:
        if (dailyAssetBalance[x][5] > 0 and (dailyAssetBalance[x][2] < walletBalance*10 or dailyAssetBalance[x][2] <15)):
            dailyAssetBalance[x][2] = round(dailyAssetBalance[x][2], 4)
            yearlyAssetBalance[x][8] = round(yearlyAssetBalance[x][8], 4)
            yearlyAssetBalance[x][9] = abs(round(yearlyAssetBalance[x][9], 4))

            totalAssetsDaily = totalAssetsDaily + dailyAssetBalance[x][5]
            dailyAssetBalance[x][5] = round(dailyAssetBalance[x][5])
            frontendDataDaily.append(dailyAssetBalance[x])

    # for x in hourlyAssetBalance:
    #     if (hourlyAssetBalance[x][5] > 0 and (hourlyAssetBalance[x][2] < walletBalance*10 or hourlyAssetBalance[x][2] <15)):
    #         hourlyAssetBalance[x][2] = round(hourlyAssetBalance[x][2], 4)
    #         yearlyAssetBalance[x][8] = round(yearlyAssetBalance[x][8], 4)
    #         yearlyAssetBalance[x][9] = abs(round(yearlyAssetBalance[x][9], 4))

    #         totalAssetsHourly = totalAssetsHourly + hourlyAssetBalance[x][5]
    #         hourlyAssetBalance[x][5] = round(hourlyAssetBalance[x][5])
    #         frontendDataHourly.append(hourlyAssetBalance[x])

    Current_Eth_response = get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    Current_Eth_data = Current_Eth_response.json()

    for x in frontendDataYearly:
        x[6] = round((x[5]/totalAssetsYearly) * 100)
        x.append(round(float(x[2]) * float(Current_Eth_data['price']),2))

    for x in frontendDataMonthly:
        x[6] = round((x[5]/totalAssetsMonthly) * 100)
        x.append(round(float(x[2]) * float(Current_Eth_data['price']),2))

    for x in frontendDataWeekly:
        x[6] = round((x[5]/totalAssetsWeekly) * 100)
        x.append(round(float(x[2]) * float(Current_Eth_data['price']),2))

    for x in frontendDataDaily:
        x[6] = round((x[5]/totalAssetsDaily) * 100)
        x.append(round(float(x[2]) * float(Current_Eth_data['price']),2))

    for x in frontendDataMax:
        x[6] = round((x[5]/totalAssetsMax) * 100)
        x.append(round(float(x[2]) * float(Current_Eth_data['price']),2))

    print("--- %s seconds ---" % (time.time() - start_time))
    return [frontendDataYearly, frontendDataMonthly, frontendDataWeekly, frontendDataDaily, round(eth_price_change,4), float(Current_Eth_data['price']), frontendDataMax]
