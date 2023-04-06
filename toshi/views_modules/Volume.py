# TODO:
#     Some Sells and Buys are not recorder in etherscan. Substitute these with other apis to fill in the link. 
#     Places marked to substiture are labbeled "alert"


import time
from ..views_modules import Misc
from requests import get
from web3 import Web3
from ..models import coinList, coinImages
from datetime import datetime
from multiprocessing import Pool
import time

FILE_NAME = 'VOLUME HISTORY OVERVIEW '
DEBUG = True
BASE_URL = "https://api.etherscan.io/api"
API_KEY = "239PUCE9PMQCURRRZPVXRBESYPF4HUHRMZ"
ETHER_VALUE = 10 ** 18
web3eth = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/21a13d88d64f420d91ff5c3272c0f8b0"))

unix_day = 86400
unix_week = 604800
unix_month = 2628000
unix_year = 31540000

# Obtain block number for retrieving data by time horizon
def get_block_number(wallet_address, custom_unix):
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    time_unix = int(currentDateAndTime - custom_unix)
    block_url = make_api_url(module="block", action="getblocknobytime",
                             wallet_address=wallet_address, closest="before", timestamp=time_unix)
    response = get(block_url)
    data = response.json()
    value = int(data["result"])
    return value

def run(walletAddress):  
    start_time = time.time()
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    checkSumwalletAddress = getCheckSumWalletAddress(walletAddress)

    # Eth to USD conversion data
    Current_Eth_response = get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    Current_Eth_data = Current_Eth_response.json()
    ethUSD = float(Current_Eth_data.get("price"))

    # Obtain block numbers
    max_block_number = 1

    # print(block_numbers)

    # year_block_number = get_block_number(checkSumwalletAddress, unix_year)
    # month_block_number = get_block_number(checkSumwalletAddress, unix_month)
    # week_block_number = get_block_number(checkSumwalletAddress, unix_week)
    # day_block_number = get_block_number(checkSumwalletAddress, unix_day)
    
    maxHistoryOverview = generateDataByTime(checkSumwalletAddress, max_block_number, ethUSD)
    # yearHistoryOverview = generateDataByTime(checkSumwalletAddress, year_block_number, ethUSD)
    # monthHistoryOverview = generateDataByTime(checkSumwalletAddress, month_block_number, ethUSD)
    # weekHistoryOverview = generateDataByTime(checkSumwalletAddress, week_block_number, ethUSD)
    # dayHistoryOverview = generateDataByTime(checkSumwalletAddress, day_block_number, ethUSD)
    
    # print(monthHistoryOverview)
    # print(weekHistoryOverview)
    # print(dayHistoryOverview)

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

    print("--- %s seconds ---" % (time.time() - start_time))
    return maxHistoryOverview

def generateDataByTime(checkSumwalletAddress, blockNumber, ethUSD):
    transactionsPerToken = dict()
    tokenDetails = dict()
    relevantTransactionsPerToken = dict()
    tokensProfitable = 0

    normalTransactions = getNormalTransactions(checkSumwalletAddress, blockNumber)
    dictNormalTransactions = convertTransactionFromArrayToDict(normalTransactions,checkSumwalletAddress, ethUSD)
    internalTransactions = getInternalTransactions(checkSumwalletAddress, blockNumber)
    dictInternalTransactions = convertTransactionFromArrayToDict(internalTransactions,checkSumwalletAddress, ethUSD)
    erc20Transactions = getERC20Transactions(checkSumwalletAddress, blockNumber)
    profitDict = getTotalTokenProfits(dictNormalTransactions,dictInternalTransactions,erc20Transactions,checkSumwalletAddress, transactionsPerToken, tokenDetails)
    totalVolumeAndTransfers = getTotalWalletVolumeAndTransfers(normalTransactions,checkSumwalletAddress)
    profitAndNegativeTotals = getTotalPositiveAndNegativeProfits(profitDict)
    historyOverview = totalVolumeAndTransfers + profitAndNegativeTotals
    
    for index,value in enumerate(historyOverview):
        historyOverview[index] = round(historyOverview[index] * ethUSD, 2)

    for k, v in profitDict.items():
        #Add one to tokens profitable if profit is greater than 0
        if v > 0:
            tokensProfitable += 1
        # We only include transactions per token that are relevant
        relevantTransactionsPerToken.update({
            k : transactionsPerToken.get(k)
        })
        # Retrieve image for that token and convert values to USD with rounding 
        imageUrl = ""
        if(coinList.objects.filter(name = k)):
            identity = coinList.objects.filter(name=k).values()[0]['identification']
            if(coinImages.objects.filter(identification = identity)):
                imageUrl = coinImages.objects.filter(identification = identity).values()[0].get("image_url")
            else:
                image_api_url = "https://api.coingecko.com/api/v3/coins/" + identity + "?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"  + "&x_cg_pro_api_key=CG-o8B8B9FoSYrQEDAoFeGveNZU"
                response = get(image_api_url)
                data = response.json()
                if(data.get("image")):
                    ci = coinImages(
                    identification=identity, 
                    image_url= data.get("image").get("thumb"), 
                    )
                    ci.save()
        elif(coinImages.objects.filter(identification = k.lower().replace(" ", "-"))):
            try:
                imageUrl = coinImages.objects.filter(identification = k.lower().replace(" ", "-")).values()[0].get("image_url")
            except:
                imageUrl = ""
        profitDict.update({
            k: [round(v * ethUSD, 2), imageUrl]
        })
        

    # Converting tokenDetails values to USD
    for value in tokenDetails.values():
        value["expense"] = value["expense"]*ethUSD

    # Appending data used for Token and Profit History Overview
    historyOverview.append(profitDict)
    historyOverview.append(tokensProfitable)
    historyOverview.append(relevantTransactionsPerToken)
    historyOverview.append(tokenDetails)
    historyOverview.append(ethUSD)

    return historyOverview


# WORK IN PROGRESS. POPULATE TABLE WITH ALL COIN IMAGES
def populateCoinImages():

    allCoins = coinList.objects.all()
    counter = 0
    for coins in allCoins:
        counter = counter + 1
        if(counter%15 == 0):
            time.sleep(60)
        identity = coins.identification
        image_url = "https://api.coingecko.com/api/v3/coins/" + identity + "?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"  + "&x_cg_pro_api_key=CG-o8B8B9FoSYrQEDAoFeGveNZU"
        response = get(image_url)
        data = response.json()
        if(data.get("image")):
            ci = coinImages(
                identification=identity, 
                image_url= data.get("image").get("thumb"), 
            )
            ci.save()
    return 1


def getTotalPositiveAndNegativeProfits(profitDict):
    positiveProfit = 0
    negativeProfit = 0
    for key in profitDict:
        profits = profitDict.get(key)
        if(profits >= 0):
            positiveProfit = positiveProfit + profits
        else:
            negativeProfit = negativeProfit + profits
    return [positiveProfit,negativeProfit]

def convertTransactionFromArrayToDict(transactions,walletAddress, ethUsd):
    txDict = dict()
    for tx in transactions:
        transactionHash = tx['hash']
        tokenAmount = float(tx["value"])/(ETHER_VALUE)
        try:
            gasPrice = float(float(tx['gasPrice']))
            gasUsed = float(float(tx['gasUsed']))
        except:
            gasPrice = 0
            gasUsed = 0
        txDict.update({
            transactionHash : tokenAmount,
            transactionHash + ".gasFees" : ((gasPrice*gasUsed)/(ETHER_VALUE))*ethUsd,
        })
    return txDict

def getTotalTokenProfits(dictNormalTransactions,dictInternalTransactions,erc20Transactions, checkSumwalletAddress, transactionsPerToken, tokenDetails):
    tokenInfo = dict()
    tokenProfit = dict()
    # Iterate through all token transfer events
    for tokensTransfers in erc20Transactions:
        tokenAllocation = float(tokensTransfers['value'])/(10 ** float(tokensTransfers['tokenDecimal']))
        # Get Token Symbol
        tokenSymbol = tokensTransfers['tokenName']
        # Get The Transaction Hash
        txHash = tokensTransfers['hash']
        # If the token is in our list
        if(tokenInfo.get(tokenSymbol) and transactionsPerToken.get(tokenSymbol)):
            transactionsPerToken.update({
                tokenSymbol: (transactionsPerToken.get(tokenSymbol) + 1)
            })
            # If the token is going to the user
            if(tokensTransfers['to'] == checkSumwalletAddress.lower()):
                # Get Token Value if it exists
                if(dictNormalTransactions.get(txHash)):
                    tokenAmount = dictNormalTransactions[txHash] / tokenAllocation
                    tokenInfo.update({
                        tokenSymbol : (tokenInfo.get(tokenSymbol) + tokenAmount)/2
                    })
                elif(coinList.objects.filter(name=tokensTransfers['tokenName'])):
                    historicalDate = coinGeckounixTimeStampToDateTime(tokensTransfers['timeStamp'])
                    identification = coinList.objects.filter(name=tokensTransfers['tokenName']).values()[0]['identification']
                    if(getPastPriceCrypto(identification,historicalDate).get("market_data")):
                        tokenEthPrice = getPastPriceCrypto(identification,historicalDate).get("market_data").get("current_price").get("eth")
                        tokenInfo.update({
                            tokenSymbol : (tokenInfo.get(tokenSymbol) + tokenEthPrice)/2
                        })
            # If the token is leaving the user, This is where we calculate profit
            elif(tokensTransfers['from'] == checkSumwalletAddress.lower()):
                # Get Token Value if it exists
                if(dictInternalTransactions.get(txHash)):
                    tokenAmount = dictInternalTransactions[txHash]
                    if(tokenProfit.get(tokenSymbol)):
                        tokenProfit.update({
                            tokenSymbol : tokenProfit.get(tokenSymbol) + (tokenAmount - (tokenInfo.get(tokenSymbol) * tokenAllocation))
                        })
                        tokenDetails.update({
                            tokenSymbol : {
                                "expense" :  tokenDetails.get(tokenSymbol)["expense"] + tokenInfo.get(tokenSymbol) * tokenAllocation,
                                "gasFees": tokenDetails.get(tokenSymbol)["gasFees"] + dictNormalTransactions[txHash+".gasFees"]
                            }
                        })
                    else:
                        tokenProfit.update({
                            tokenSymbol : tokenAmount - (tokenInfo.get(tokenSymbol) * tokenAllocation) 
                        })
                        tokenDetails.update({
                            tokenSymbol : {
                                "expense" : tokenInfo.get(tokenSymbol) * tokenAllocation,
                                "gasFees": dictNormalTransactions[txHash+".gasFees"]
                            }
                        })
                elif(coinList.objects.filter(name=tokensTransfers['tokenName'])):
                    historicalDate = coinGeckounixTimeStampToDateTime(tokensTransfers['timeStamp'])
                    identification = coinList.objects.filter(name=tokensTransfers['tokenName']).values()[0]['identification']
                    if(getPastPriceCrypto(identification,historicalDate).get("market_data")):
                        tokenEthPrice = getPastPriceCrypto(identification,historicalDate).get("market_data").get("current_price").get("eth")
                        if(tokenProfit.get(tokenSymbol)):
                            tokenProfit.update({
                                tokenSymbol : tokenProfit.get(tokenSymbol) + (tokenAmount - (tokenEthPrice * tokenAllocation))
                            })
                            if(tokenDetails.get(tokenSymbol) and tokenDetails.get(tokenSymbol)["gasFees"]):
                                tokenDetails.update({
                                    tokenSymbol : {
                                        "expense" : tokenDetails.get(tokenSymbol)["expense"] + tokenEthPrice * tokenAllocation,
                                        "gasFees" : tokenDetails.get(tokenSymbol)["gasFees"]
                                    }
                                })
                        else:
                            tokenProfit.update({
                                tokenSymbol : tokenAmount - (tokenEthPrice * tokenAllocation) 
                            })
                            if(tokenDetails.get(tokenSymbol) and tokenDetails.get(tokenSymbol)["gasFees"]):
                                tokenDetails.update({
                                    tokenSymbol : {
                                        "expense" : tokenEthPrice * tokenAllocation,
                                        "gasFees" : tokenDetails.get(tokenSymbol)["gasFees"]
                                    }
                                })
        # If the token is not in our list
        else:
            transactionsPerToken.update({
                tokenSymbol: 1
            })
            # Get Token Value if it exists
            if(dictNormalTransactions.get(txHash) and tokenAllocation != 0 ):
                tokenAmount = dictNormalTransactions[txHash] / tokenAllocation
                # If the token is going to the user
                if(tokensTransfers['to'] == checkSumwalletAddress.lower()):
                    tokenInfo.update({
                        tokenSymbol : tokenAmount 
                    })
            # If the token does not exist, we check coingecko
            else:
                # If the token is going to the user
                if(tokensTransfers['to'] == checkSumwalletAddress.lower()):
                    if(tokensTransfers['tokenName'] == "Tether USD"):
                        tokenInfo.update({
                            tokenSymbol : tokenAllocation 
                        })
                    elif(coinList.objects.filter(name=tokensTransfers['tokenName'])):
                        historicalDate = coinGeckounixTimeStampToDateTime(tokensTransfers['timeStamp'])
                        identification = coinList.objects.filter(name=tokensTransfers['tokenName']).values()[0]['identification']
                        if(getPastPriceCrypto(identification,historicalDate).get("market_data")):
                            tokenEthPrice = getPastPriceCrypto(identification,historicalDate).get("market_data").get("current_price").get("eth")
                            tokenInfo.update({
                                tokenSymbol : tokenEthPrice
                            })
    return tokenProfit

def coinGeckounixTimeStampToDateTime(unix):
    return (
        datetime.fromtimestamp(
            int(unix)
        ).strftime('%d-%m-%Y')
    )

def getPastPriceCrypto(identification, date):
    url = "https://pro-api.coingecko.com/api/v3/coins/" + identification + "/history?date=" + date + "&localization=false" + "&x_cg_pro_api_key=CG-o8B8B9FoSYrQEDAoFeGveNZU"
    response = get(url)
    data = response.json()
    return data

def getCheckSumWalletAddress(nonCheckSumWalletAddress):
    return Web3.toChecksumAddress('0x' + str(nonCheckSumWalletAddress[-40:]))

def getTotalWalletVolumeAndTransfers(tx, walletAddress):
    totalVolume = 0
    totalTransfersIn = 0
    totalTransfersOut = 0
    
    for transactions in tx:
        if(transactions['to'] == walletAddress.lower()):
            totalTransfersIn = totalTransfersIn + float(transactions['value'])/ETHER_VALUE
        elif(transactions['from'] == walletAddress.lower()):
            totalTransfersOut = totalTransfersOut + float(transactions['value'])/ETHER_VALUE
        totalVolume = totalVolume + float(transactions['value'])/ETHER_VALUE
    return [totalVolume,totalTransfersIn,totalTransfersOut]

def getNormalTransactions(walletAddress, blockNumber):
    transactions_url = make_api_url(
        "account", 
        "txlist", 
        walletAddress,
        startblock=blockNumber, 
        endblock=99999999, 
        page=1, 
        offset=2000, 
        sort="asc"
    )
    response = get(transactions_url)
    data = response.json()["result"]
    return data

def getInternalTransactions(walletAddress, blockNumber):
    transactions_url = make_api_url(
        "account", 
        "txlistinternal", 
        walletAddress,
        startblock=blockNumber, 
        endblock=99999999, 
        page=1, 
        offset=2000, 
        sort="asc"
    )
    response = get(transactions_url)
    data = response.json()["result"]
    return data

def getERC20Transactions(walletAddress, blockNumber):
    transactions_url = make_api_url(
        "account", 
        "tokentx", 
        walletAddress,
        startblock=blockNumber, 
        endblock=99999999, 
        page=1, 
        offset=2000, 
        sort="asc"
    )
    response = get(transactions_url)
    data = response.json()["result"]
    return data

def make_api_url(module, action, wallet_address, **kwargs):
    url = BASE_URL + \
        f"?module={module}&action={action}&address={wallet_address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url

def getPastPriceCrypto(identification, date):
    url = "https://pro-api.coingecko.com/api/v3/coins/" + identification + "/history?date=" + date + "&localization=false" + "&x_cg_pro_api_key=CG-o8B8B9FoSYrQEDAoFeGveNZU"
    response = get(url)
    data = response.json()
    return data