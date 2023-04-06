from ..views_modules import Misc
from requests import get
import time

from requests import get
from datetime import datetime
from channels.layers import get_channel_layer
from Historic_Crypto import LiveCryptoData
from web3 import Web3
import json
import time as t
import pandas as pd
from syncer import sync


FILE_NAME = 'PersonalPerformanceGraph'
DEBUG = True
API_KEY = "239PUCE9PMQCURRRZPVXRBESYPF4HUHRMZ"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18
ALCHEMY_API = "_mEa4ksrzCdb8fgB5_7-4doIZrMWwpKf"
ETHPLORER_API = "EK-joHSG-JyCU9Ay-jsqCh"
NUM_RETRIES = 30
RETRY_DELAY = 1.2
unix_hour = 3600
unix_day = 86400
unix_week = 604800
unix_month = 2628000
unix_year = 31540000

web3ethAlchemy = Web3(Web3.HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/_mEa4ksrzCdb8fgB5_7-4doIZrMWwpKf"))
# ABI
erc20TokenAbi = [{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"payable":True,"stateMutability":"payable","type":"fallback"},{"anonymous":False,"inputs":[{"indexed":True,"name":"owner","type":"address"},{"indexed":True,"name":"spender","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]
uniswapAbi = [{"inputs": [],"name": "getReserves","outputs": [{"internalType": "uint112","name": "_reserve0","type": "uint112"},{"internalType": "uint112","name": "_reserve1","type": "uint112"},{"internalType": "uint32","name": "_blockTimestampLast","type": "uint32"}],"stateMutability": "view","type": "function"},{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
uniswap_v3_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]')


def run(walletAddress):
    FUNCTION_NAME = 'run'

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    checkSumwalletAddress = getCheckSumWalletAddress(walletAddress)
    currentDateAndTime = t.mktime(datetime.now().timetuple())
    maxNormalTransactions = getMaxNormalTransactions(checkSumwalletAddress)
    maxInternalTransactions = getMaxInternalTransactions(checkSumwalletAddress)
    combinedTransactions = combineAndSort(maxNormalTransactions,maxInternalTransactions)
    graph = getGraphData(combinedTransactions, checkSumwalletAddress,currentDateAndTime)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
    return graph

def combineAndSort(normalTransactions, internalTransactions):
    combinedTransactions = normalTransactions + internalTransactions
    combinedTransactions.sort(key=lambda x: int(x['timeStamp']))
    return combinedTransactions


def getCurrentBalance(walletAddress, ethToUsd):
    provider_url = 'https://falling-ultra-wind.discover.quiknode.pro/40967b3f0385508346c8ec08d2c43faa7fec6f8e/'
    w3 = Web3(Web3.HTTPProvider(provider_url))
    blockNumber = w3.eth.blockNumber
    startingBalance = w3.eth.get_balance(walletAddress, blockNumber)
    startingBalanceUsd = float(w3.fromWei(startingBalance, "ether"))*ethToUsd
    print(startingBalanceUsd)
    return startingBalanceUsd
    

def getGraphData(transactions, walletAddress,currentTime):
    
    ethToUsd = getEthToUSD()
    current_balance = getCurrentBalance(walletAddress, ethToUsd)
    balance_today = current_balance
    daily_filtered_object_balance = []
    weekly_filtered_object_balance = []
    monthly_filtered_object_balance = []
    yearly_filtered_object_balance = []
    max_filtered_object_balance = []

    last_day = int(currentTime - unix_day)
    last_week = int(currentTime - unix_week)
    last_month = int(currentTime - unix_month)
    last_year = int(currentTime - unix_year)
    
    def createTicks(unix, divisions):
        time_array = []
        timestamp = t.time()
        for _ in range(divisions):
            time_array.append(timestamp)
            timestamp -= unix
        return time_array
    
    # One Year
    yearTicks = createTicks(unix_month, 48)
    # One Month
    monthTicks = createTicks(unix_week, 6)
    # One Week
    weekTicks = createTicks(unix_day, 7)
    # One Day
    dayTicks = createTicks(unix_hour, 24)

    for tx in reversed(transactions):
        gas = 1
        fromUser = tx.get("from")
        toUser = tx.get("to")
        time = str(tx.get('timeStamp'))
        integerTime = int(time)
        time_name = coinGeckounixTimeStampToDateTime(time)
        value = (int(tx.get("value")) / ETHER_VALUE) * ethToUsd

        if "gasPrice" in tx:
            gas = (int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE)* ethToUsd
        else:
            gas = (int(tx["gasUsed"]) / ETHER_VALUE)* ethToUsd
        
        if(fromUser == walletAddress.lower()):
            current_balance = current_balance + value + gas
        elif(toUser == walletAddress.lower()):
            current_balance = current_balance - value
        
        max_filtered_object_balance.append({
            "time" : (int(time)),
            "USD": int(current_balance) ,
            "ETH": int(current_balance)/ethToUsd,
            "time_name": time_name,
            "time_formatted": datetime.fromtimestamp(int(time)).strftime("%m/%y")
        })

        if integerTime > last_year:    
            yearly_filtered_object_balance.append({
                "time" : (int(time)),
                "USD": int(current_balance),
                "ETH": int(current_balance)/ethToUsd,
                "time_name": time_name,
                "time_formatted": datetime.fromtimestamp(int(time)).strftime("%m/%y")
            })

        if integerTime > last_day:    
            daily_filtered_object_balance.append({
                "time" : (int(time)),
                "USD": int(current_balance),
                "ETH": int(current_balance)/ethToUsd,
                "time_name": time_name,
                "time_formatted": datetime.fromtimestamp(int(time)).strftime("%H") + ":00" 
            })

        if integerTime > last_week:    
            weekly_filtered_object_balance.append({
                "time" : (int(time)),
                "USD": int(current_balance),
                "ETH": int(current_balance)/ethToUsd,
                "time_name": time_name,
                "time_formatted": datetime.fromtimestamp(int(time)).strftime("%b %-d")
            })

        if integerTime > last_month:    
            monthly_filtered_object_balance.append({
                "time" : (int(time)),
                "USD": int(current_balance),
                "ETH": int(current_balance)/ethToUsd,
                "time_name": time_name,
                "time_formatted": datetime.fromtimestamp(int(time)).strftime("%b %-d")
            })
    
    def obtainRange(balance):
        try:
            result = [min(balance, key=lambda x:x['USD']), max(balance, key=lambda x:x['USD'])]
        except: 
            result = [0,0]
        return result

    rangeMaxBalance = obtainRange(max_filtered_object_balance)
    rangeYearlyBalance = obtainRange(yearly_filtered_object_balance)
    rangeMonthlyBalance = obtainRange(monthly_filtered_object_balance)
    rangeWeeklyBalance = obtainRange(weekly_filtered_object_balance)
    rangeDailyBalance = obtainRange(daily_filtered_object_balance)

    # backward fill max_filtered_object_balance by adding one more datapoint


    if len(max_filtered_object_balance) > 0:
        max_filtered_object_balance.insert(0, {
            "time" : (int(t.time())),
            "USD": round(balance_today, 2),
            "ETH": balance_today/ethToUsd,
            "time_name": time_name,
            "time_formatted": datetime.fromtimestamp(int(time)).strftime("%m/%y")
        })

        max_filtered_object_balance.append({
            "time" : (max_filtered_object_balance[-1]["time"] - 600),
            "USD": 0,
            "ETH": 0
        })

        max_filtered_object_balance.append({
            "time" : 1451691024,
            "USD": 0,
            "ETH": 0
        })
        
    return [
        max_filtered_object_balance,
        [rangeMaxBalance, rangeYearlyBalance, rangeMonthlyBalance, rangeWeeklyBalance, rangeDailyBalance],
        [yearTicks, monthTicks, weekTicks, dayTicks]
    ]

def getCheckSumWalletAddress(nonCheckSumWalletAddress):
    return Web3.toChecksumAddress('0x' + str(nonCheckSumWalletAddress[-40:]))

def getMaxNormalTransactions(walletAddress):
    transactions_url = make_api_url(
        "account",
        "txlist",
        walletAddress,
        startblock=0,
        endblock=99999999,
        page=1,
        offset=10000,
        sort="asc"
    )
    response = get(transactions_url)
    data = response.json()["result"]
    return data

def getMaxInternalTransactions(walletAddress):
    transactions_url = make_api_url(
        "account",
        "txlistinternal",
        walletAddress,
        startblock=0,
        endblock=99999999,
        page=1,
        offset=10000,
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

def getEthToUSD():
    
    # Set the addresses of the token, exchange contracts, Eth, and USD
    uniswap_exchange_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D' # Uniswap router v2 contract address
    eth_contract_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' # wEth contract address
    tokenAddress = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    # Get the contract instances for the token and exchange
    exchange_contract = web3ethAlchemy.eth.contract(address=uniswap_exchange_address, abi=(json.dumps(uniswapAbi)))
    token = web3ethAlchemy.eth.contract(address=tokenAddress, abi=json.loads(json.dumps(erc20TokenAbi))) # declaring the token contract
    # Get the token decimal
    token_decimals = 6
    exchange_decimal = 18

    # Set the input ammount
    token_input_amount = (10**token_decimals)

    # Set Path
    token_path = [tokenAddress, eth_contract_address] # TOKEN -> ETH

    # Set the token exchange rates
    token_to_eth_price_wei = [0,0]

    try:
        # Get the token exchange rates
        token_to_eth_price_wei = exchange_contract.functions.getAmountsOut(token_input_amount, token_path).call()
    except Exception as e:
        errorMessage = e.args[0]
        if(errorMessage == "execution reverted"):
            # If there's an error, retry the API call
            for i in range(NUM_RETRIES):
                time.sleep(RETRY_DELAY)
                try:
                    token_to_eth_price_wei = exchange_contract.functions.getAmountsOut(token_input_amount, token_path).call()
                except:
                    print(f"Retrying API call in {RETRY_DELAY} seconds...")


    # Get the token exhange rates in the proper units
    token_to_eth_price_eth = token_to_eth_price_wei[1]/((10**exchange_decimal))
    ethUSD = 1/token_to_eth_price_eth
    return ethUSD

def coinGeckounixTimeStampToDateTime(unix):
    return (
        datetime.fromtimestamp(
            int(unix)
        ).strftime('%d-%m-%Y')
    )