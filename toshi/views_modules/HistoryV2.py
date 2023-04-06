from ..views_modules import Misc
import json
from requests import get
from web3 import Web3
from ..models import coinList, coinImages
from datetime import datetime
import time
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor

tokenBuyingPrice = dict()
priceAndAsset = dict()
FILE_NAME = 'HISTORY PAGE OVERVIEW '
DEBUG = True
BASE_URL = "https://api.etherscan.io/api"
API_KEY = "239PUCE9PMQCURRRZPVXRBESYPF4HUHRMZ"
ETHER_VALUE = 10 ** 18
web3ethAlchemy = Web3(Web3.HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/_mEa4ksrzCdb8fgB5_7-4doIZrMWwpKf"))
# web3ethInfura= Web3(Web3.HTTPProvider(" https://mainnet.infura.io/v3/21a13d88d64f420d91ff5c3272c0f8b0"))
# Define the number of retries and delay between retries
NUM_RETRIES = 8
RETRY_DELAY = 1
unix_day = 86400
unix_week = 604800
unix_month = 2628000
unix_year = 31540000
erc20TokenAbi = [{"constant":True,"inputs":[],"name":"holders","outputs":[{"name":"","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant": True,"inputs": [],"name": "totalSupply","outputs": [{"name": "","type": "uint256"}],"payable": False,"stateMutability": "view","type": "function"},{"anonymous": False,"inputs": [{ "indexed": True, "name": "from", "type": "address" },{ "indexed": True, "name": "to", "type": "address" },{ "indexed": False, "name": "value", "type": "uint256" }],"name": "Transfer","type": "event"},{"inputs": [{"internalType": "address","name": "recipient","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "transfer","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable": False,"stateMutability": "nonpayable","type": "function","cache_call": True}]
uniswapAbi = [{"inputs": [],"name": "getReserves","outputs": [{"internalType": "uint112","name": "_reserve0","type": "uint112"},{"internalType": "uint112","name": "_reserve1","type": "uint112"},{"internalType": "uint32","name": "_blockTimestampLast","type": "uint32"}],"stateMutability": "view","type": "function"},{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
uniswap_v3_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]')


def run(walletAddress):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    start_time = time.time()
    # Eth to USD conversion data
    Current_Eth_response = get(
        "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    Current_Eth_data = Current_Eth_response.json()
    ethUSD = float(Current_Eth_data.get("price"))

    # Get the checksum wallet address
    checksumWalletAddress = getCheckSumWalletAddress(walletAddress)
    # Get Transactions using API call
    maxERC20Transactions = getMaxERC20Transactions(checksumWalletAddress)
    maxNormalTransactions = getMaxNormalTransactions(checksumWalletAddress)
    maxInternalTransactions = getMaxInternalTransactions(checksumWalletAddress)

    # Split time into daily, weekly, monthly, and yearly
    dailyERC20Transactions, weeklyERC20Transactions, monthlyERC20Transactions, yearlyERC20Transactions = splitTimes(
        maxERC20Transactions)
    dailyNormalTransactions, weeklyNormalTransactions, monthlyNormalTransactions, yearlyNormalTransactions = splitTimes(
        maxNormalTransactions)
    dailyInternalTransactions, weeklyInternalTransactions, monthlyInternalTransactions, yearlyInternalTransactions = splitTimes(
        maxInternalTransactions)

    # Convert each time array into dict
    dailyDictNormalTransactions = convertTransactionFromArrayToDict(dailyNormalTransactions)
    weeklyDictNormalTransactions = convertTransactionFromArrayToDict(weeklyNormalTransactions)
    monthlyDictNormalTransactions = convertTransactionFromArrayToDict(monthlyNormalTransactions)
    yearlyDictNormalTransactions = convertTransactionFromArrayToDict(yearlyNormalTransactions)
    maxDictNormalTransactions = convertTransactionFromArrayToDict(maxNormalTransactions)
    dailyDictInternalTransactions = convertTransactionFromArrayToDict(dailyInternalTransactions)
    weeklyDictInternalTransactions = convertTransactionFromArrayToDict(weeklyInternalTransactions)
    monthlyDictInternalTransactions = convertTransactionFromArrayToDict(monthlyInternalTransactions)
    yearlyDictInternalTransactions = convertTransactionFromArrayToDict(yearlyInternalTransactions)
    maxDictInternalTransactions = convertTransactionFromArrayToDict(maxInternalTransactions)
    # GET INCOMPLETE TOKEN LIST
    maxDetailedTokens = getTokenDetailsAndProfit(maxERC20Transactions,maxDictNormalTransactions,maxDictInternalTransactions,checksumWalletAddress,ethUSD)
    yearlyDetailedTokens = getTokenDetailsAndProfit(yearlyERC20Transactions,yearlyDictNormalTransactions,yearlyDictInternalTransactions,checksumWalletAddress,ethUSD)
    monthlyDetailedTokens = getTokenDetailsAndProfit(monthlyERC20Transactions,monthlyDictNormalTransactions,monthlyDictInternalTransactions,checksumWalletAddress,ethUSD)
    weeklyDetailedTokens = getTokenDetailsAndProfit(weeklyERC20Transactions,weeklyDictNormalTransactions,weeklyDictInternalTransactions,checksumWalletAddress,ethUSD)
    dailyDetailedTokens = getTokenDetailsAndProfit(dailyERC20Transactions,dailyDictNormalTransactions,dailyDictInternalTransactions,checksumWalletAddress,ethUSD)
    # SORT PROFIT LIST
    sortedMaxDetailedTokens = sortTokenDetailsAndProfit(maxDetailedTokens)
    sortedYearlyDetailedTokens = sortTokenDetailsAndProfit(yearlyDetailedTokens)
    sortedMonthlyDetailedTokens = sortTokenDetailsAndProfit(monthlyDetailedTokens)
    sortedWeeklyDetailedTokens = sortTokenDetailsAndProfit(weeklyDetailedTokens)
    sortedDailyDetailedTokens = sortTokenDetailsAndProfit(dailyDetailedTokens)
  
    # GET TOKEN ALLOTMENT AND MARKET PRICE IN ETH
    maxTokenAllotmentAndMarketPrice = getTokenAllotmentAndMarketPrice(sortedMaxDetailedTokens,checksumWalletAddress)
    yearlyTokenAllotmentAndMarketPrice = getTokenAllotmentAndMarketPrice(sortedYearlyDetailedTokens,checksumWalletAddress)
    monthlyTokenAllotmentAndMarketPrice = getTokenAllotmentAndMarketPrice(sortedMonthlyDetailedTokens,checksumWalletAddress)
    weeklyTokenAllotmentAndMarketPrice = getTokenAllotmentAndMarketPrice(sortedWeeklyDetailedTokens,checksumWalletAddress)
    dailyTokenAllotmentAndMarketPrice = getTokenAllotmentAndMarketPrice(sortedDailyDetailedTokens,checksumWalletAddress)
    # GET TOKEN HISTORY OVERVIEW
    maxCompletedDetailedTokens = completeDetailedTokens(sortedMaxDetailedTokens,maxTokenAllotmentAndMarketPrice,ethUSD)
    yearlyCompletedDetailedTokens = completeDetailedTokens(sortedYearlyDetailedTokens,yearlyTokenAllotmentAndMarketPrice,ethUSD)
    monthlyCompletedDetailedTokens = completeDetailedTokens(sortedMonthlyDetailedTokens,monthlyTokenAllotmentAndMarketPrice,ethUSD)
    weeklyCompletedDetailedTokens = completeDetailedTokens(sortedWeeklyDetailedTokens,weeklyTokenAllotmentAndMarketPrice,ethUSD)
    dailyCompletedDetailedTokens = completeDetailedTokens(sortedDailyDetailedTokens,dailyTokenAllotmentAndMarketPrice,ethUSD)
    # GET PROFIT HISTORY OVERVIEW
    maxProfitHistoryOverview = getProfitHistoryOverview(maxCompletedDetailedTokens,maxNormalTransactions,checksumWalletAddress,ethUSD)
    yearlyProfitHistoryOverview = getProfitHistoryOverview(yearlyCompletedDetailedTokens,yearlyNormalTransactions,checksumWalletAddress,ethUSD)
    monthlyProfitHistoryOverview = getProfitHistoryOverview(monthlyCompletedDetailedTokens,monthlyNormalTransactions,checksumWalletAddress,ethUSD)
    weeklyProfitHistoryOverview = getProfitHistoryOverview(weeklyCompletedDetailedTokens,weeklyNormalTransactions,checksumWalletAddress,ethUSD)
    dailyProfitHistoryOverview = getProfitHistoryOverview(dailyCompletedDetailedTokens,dailyNormalTransactions,checksumWalletAddress,ethUSD)
    # GET VOLUME HISTORY OVERVIEW
    maxVolumeHistoryOverview = getVolumeHistoryOverview(maxCompletedDetailedTokens,maxNormalTransactions,checksumWalletAddress,ethUSD)
    yearlyVolumeHistoryOverview = getVolumeHistoryOverview(yearlyCompletedDetailedTokens,yearlyNormalTransactions,checksumWalletAddress,ethUSD)
    monthlyVolumeHistoryOverview = getVolumeHistoryOverview(monthlyCompletedDetailedTokens,monthlyNormalTransactions,checksumWalletAddress,ethUSD)
    weeklyVolumeHistoryOverview = getVolumeHistoryOverview(weeklyCompletedDetailedTokens,weeklyNormalTransactions,checksumWalletAddress,ethUSD)
    dailyVolumeHistoryOverview = getVolumeHistoryOverview(dailyCompletedDetailedTokens,dailyNormalTransactions,checksumWalletAddress,ethUSD)
    historyResponse = [
        [
            dailyProfitHistoryOverview,
            weeklyProfitHistoryOverview,
            monthlyProfitHistoryOverview,
            yearlyProfitHistoryOverview,
            maxProfitHistoryOverview,
        ],
        [
            dailyVolumeHistoryOverview,
            weeklyVolumeHistoryOverview,
            monthlyVolumeHistoryOverview,
            yearlyVolumeHistoryOverview,
            maxVolumeHistoryOverview,
        ],
        [
            dailyCompletedDetailedTokens,
            weeklyCompletedDetailedTokens,
            monthlyCompletedDetailedTokens,
            yearlyCompletedDetailedTokens,
            maxCompletedDetailedTokens,
        ]
    ]
    print("--- %s seconds ---" % (time.time() - start_time))
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
    return historyResponse

def sortTokenDetailsAndProfit(tokensAndProfitList):
    sorted_dict = {k: v for k, v in sorted(tokensAndProfitList.items(), key=lambda item: item[1][5], reverse=True )}
    return sorted_dict
def getMarketPriceAssetAllocation(tokenAddressAndDecimal,walletAddress):
    # Set the addresses of the token, exchange contracts, Eth, and USD
    uniswap_exchange_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D' # Uniswap router v2 contract address
    eth_contract_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' # wEth contract address
    # Create a contract instance for the Uniswap Router v3
    uniswap_v3_router_address = '0xE592427A0AEce92De3Edee1F18E0157C05861564'
    uniswap_v3_router = web3ethAlchemy.eth.contract(address=uniswap_v3_router_address, abi=uniswap_v3_router_abi)

    # Set Fee
    fee = 3000 # 0.3% fee
    # Set price limit
    sqrt_price_limitx96 = 0 # No price limit
    # Set deadline
    deadline = int(web3ethAlchemy.eth.getBlock('latest').timestamp) + 300 # Transaction deadline 300 seconds from now
    # Define the maximum amount of WETH that we are willing to receive in exchange
    amount_out_min = 0
    # Define the wallet addresses and private key
    WALLET_ADDRESS = '0x1CAb3C4ad653148f15B4ad8D7b5BD96ad968279c'
    WALLET_PRIVATE_KEY = '7ba6f3a0ff3b3b8f836de52be913fad29781685a6e640991624e8d3adaf92b0d'
    # Set up the account
    account = web3ethAlchemy.eth.account.privateKeyToAccount(WALLET_PRIVATE_KEY)

    tokenAddress = tokenAddressAndDecimal[0]


    if(priceAndAsset.get(tokenAddress)):
        return priceAndAsset

    if(tokenAddress == eth_contract_address):
        rawBalance = -1
        token = web3ethAlchemy.eth.contract(address=tokenAddress, abi=json.loads(json.dumps(erc20TokenAbi))) # declaring the token contract
        try:
            rawBalance = token.functions.balanceOf(walletAddress).call()
        except:
            # print("BALANCE EXCEPTION")
            # If there's an error, retry the API call
            for i in range(NUM_RETRIES):
                # print(f"Retrying API call in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
                try:
                    rawBalance = token.functions.balanceOf(walletAddress).call()
                except:
                    print(f"Error on attempt {i+1}")
        balance = rawBalance / (10 ** 18)
        priceAndAsset.update({
            tokenAddress : [
                balance,1
            ]
        })
        return priceAndAsset

    # Get the contract instances for the token and exchange
    exchange_contract = web3ethAlchemy.eth.contract(address=uniswap_exchange_address, abi=(json.dumps(uniswapAbi)))
    token = web3ethAlchemy.eth.contract(address=tokenAddress, abi=json.loads(json.dumps(erc20TokenAbi))) # declaring the token contract
    # Get the token decimal
    token_decimals = int(tokenAddressAndDecimal[1])
    exchange_decimal = 18

    # Set the input ammount
    token_input_amount = (10**token_decimals)

    # Set Path
    token_path = [tokenAddress, eth_contract_address] # TOKEN -> ETH

    # Set the token exchange rates
    token_to_eth_price_wei = [0,0]

    # Set the token balance in wei
    rawBalance = -1
    paramTuple = [
        tokenAddress,
        eth_contract_address,
        fee,
        (10**token_decimals),
        amount_out_min,
        account.address,
        sqrt_price_limitx96,
        deadline
    ]
    # paramTuple = {
    #     'tokenIn': tokenAddress,
    #     'tokenOut': eth_contract_address,
    #     'fee': fee,
    #     'recipient': account.address,
    #     'deadline': deadline,
    #     'amountIn': 10000* (10**token_decimals),
    #     'amountOutMinimum': amount_out_min,
    #     'sqrtPriceLimitX96': sqrt_price_limitx96
    # }
    # getMarketDataUsingRouterV3(paramTuple=paramTuple, uniswap_v3_router=uniswap_v3_router)


    try:
        # Get the token balance in wei
        rawBalance = token.functions.balanceOf(walletAddress).call()
    except:
        # print("BALANCE EXCEPTION")
        # If there's an error, retry the API call
        for i in range(NUM_RETRIES):
            # print(f"Retrying API call in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
            try:
                # Get the token balance in wei
                rawBalance = token.functions.balanceOf(walletAddress).call()
            except:
                print("COULD NOT GET BALANCE")


    # Get balance in token amount
    balance = rawBalance / (10 ** token_decimals)
    if(balance < 0.01):
        priceAndAsset.update({
            tokenAddress : [
                balance,0
            ]
        })
        return priceAndAsset

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
        else:
            # getTransactionEthFromBlockchain(tokenAddress)
            token_to_eth_price_wei[1] = (getTransactionEthFromBlockchain(tokenAddress))
            # getMarketDataUsingRouterV3(paramTuple=paramTuple, uniswap_v3_router=uniswap_v3_router)
            # print("----------------------------------- CONTRACT EXCEPTION -----------------------------------")
            # print("RETURNED ADDRESS: ", tokenAddress)
            # print("RETURNED VALUE: ", token_to_eth_price_wei)
            # print("----------------------------------- CONTRACT EXCEPTION -----------------------------------")


    # Get the token exhange rates in the proper units
    token_to_eth_price_eth = token_to_eth_price_wei[1]/((10**exchange_decimal))

    priceAndAsset.update({
        tokenAddress : [
            balance,token_to_eth_price_eth
        ]
    })

    return priceAndAsset

# def getMarketDataUsingRouterV3(paramTuple, uniswap_v3_router):
#     tx_params = {
#         # what is this even used for?
#         'value': web3ethAlchemy.toWei(0.000001, 'ether'),
#     }
#     # res = uniswap_v3_router.functions.exactInputSingle(
#     #     paramTuple
#     # ).buildTransaction(
#     #     tx_params
#     # )

#     print("-----------------------------------------")
#     print("param: ", paramTuple)
#     print("UNIswap router v3: ", uniswap_v3_router)
#     print("-----------------------------------------")
#     try:
#         print("param: ", paramTuple)
#         print("UNIswap router v3: ", uniswap_v3_router)
#         # Call the exact_input_single function to perform the swap
#         print("**************************************")
#         swap_result = uniswap_v3_router.functions.exactInputSingle(
#             paramTuple[0],
#             paramTuple[1],
#             paramTuple[2],
#             paramTuple[3],
#             paramTuple[4],
#             paramTuple[5],
#             paramTuple[6]
#         ).call()

#         print("SWAP RESULTS: ", swap_result)
#         amount_out = swap_result[1]
#         print("**************************************")
#         print(f"Amount of WETH received: {amount_out}")
#     except Exception as e:
#         errorMessage = e.args
#         print("ROUTER V3: ", errorMessage)
#         if(errorMessage == "execution reverted"):
#             # If there's an error, retry the API call
#             for i in range(NUM_RETRIES):
#                 time.sleep(RETRY_DELAY)
#                 try:
#                     # Call the exact_input_single function to perform the swap
#                     print("**************************************")
#                     swap_result = uniswap_v3_router.functions.exactInputSingle(
#                         paramTuple[0],
#                         paramTuple[1],
#                         paramTuple[2],
#                         paramTuple[3],
#                         paramTuple[4],
#                         paramTuple[5],
#                         paramTuple[6]
#                     ).call()
#                     print("SWAP RESULTS: ", swap_result)
#                     amount_out = swap_result[1]
#                     print(f"Amount of WETH received: {amount_out}")
#                     print("**************************************")
#                 except Exception as e:
#                     print("INNER ROUTER V3: ", e.args[0])
#                     print(f"INNER ROUTER V3 Retrying API call in {RETRY_DELAY} seconds...")
#         else:
#             print("RETRY")
#             print(e.args)

def getTransactionEthFromBlockchain(token_address):
    # print("----------------------------")
    # Get the contract instances for the token
    token = web3ethAlchemy.eth.contract(address=token_address, abi=json.loads(json.dumps(erc20TokenAbi))) # declaring the token contract
    # Get the token decimal
    # print("TOKEN: ", token)
    exchange_decimal = 18
    latest_block = web3ethAlchemy.eth.block_number
    # print("LATEST BLOCK: ", latest_block)
    event_filter = token.events.Transfer.createFilter(fromBlock=0)
    # event_filter = token.events.Transfer.createFilter(fromBlock=latest_block-1000)
    # print("EVENT FILTER: ", event_filter)
    events = event_filter.get_all_entries()
    # print("EVENTS: ", events)
    before = 0
    after = 0
    if len(events) > 0:
        most_recent_event = events[-1]
        tx_hash = most_recent_event['transactionHash'].hex()
        # print("TRANSACTION HASH: ", tx_hash)
        # print("TOKEN ADDRESS: ", token_address)
        block_number = web3ethAlchemy.eth.getTransaction(tx_hash).blockNumber
        from_user = most_recent_event['args']['from']
        # print("from_user: ", from_user)
        # print("block_number: ", block_number)
        try:
            before = web3ethAlchemy.eth.get_balance(from_user, block_number-1)
            after = web3ethAlchemy.eth.get_balance(from_user, block_number+1)
            print("before: ", before)
            print("after: ", after)
        except:
            # If there's an error, retry the API call
            for i in range(NUM_RETRIES):
                # print(f"Retrying API call in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
                try:
                    before = web3ethAlchemy.eth.get_balance(from_user, block_number-1)
                    after = web3ethAlchemy.eth.get_balance(from_user, block_number+1)
                except:
                    print("retry")
    # print("----------------------------")
    return ((abs(after - before))/(10 ** exchange_decimal))

def getTokenAllotmentAndMarketPrice(tokenList,walletAddress):
    tokenAllotmentAndMarketPrice = dict()
    contractAddressList = []

    for tokens in tokenList:
        tokenArray = tokenList.get(tokens)
        # TOKEN AMOUNT
        tokenAmount = tokenArray[4]
        tokenDecimal = tokenArray[11]
        contractAddress = tokenArray[2]
        contractAddressList.append([contractAddress,tokenDecimal,tokenAmount])
        tokenAllotmentAndMarketPrice.update({
            contractAddress: [
                0, # Market Price
                tokenAmount # Token Allotment
            ]
        })

    with concurrent.futures.ThreadPoolExecutor() as executor:
        assetsAndMarketPrice = {executor.submit(getMarketPriceAssetAllocation, contractAddressList, walletAddress): contractAddressList for contractAddressList in contractAddressList}
        for future in concurrent.futures.as_completed(assetsAndMarketPrice):
            assetAndPrice = assetsAndMarketPrice[future]
            if(not future.exception()):
                data = future.result()
                tokenAssetArray = tokenAllotmentAndMarketPrice.get(assetAndPrice[0])
                # print("---------------------------")
                # print(future.exception())
                # print(assetAndPrice)
                # print("CONTRACT ADDRESS, TOKEN DECIMAL: ", assetAndPrice)
                # print("Market Price, Holdings: ", tokenAssetArray)
                tokenAssetArray[0] = data.get(assetAndPrice[0])[1]
                tokenAssetArray[1] = data.get(assetAndPrice[0])[0]
                # print("Market Price, Holdings: ", tokenAssetArray)
                # print("---------------------------")

    return tokenAllotmentAndMarketPrice

def getVolumeHistoryOverview(maxDetailedTokens,maxNormalTransactions,checksumWalletAddress,ethUSD):
    totalVolume, totalTransfersIn, totalTransfersOut = getTotalWalletVolumeAndTransfers(maxNormalTransactions,checksumWalletAddress)
    positiveProfit,negativeProfit = getTotalPositiveAndNegativeProfits(maxDetailedTokens)
    return [totalVolume*ethUSD,totalTransfersIn*ethUSD,totalTransfersOut*ethUSD,positiveProfit,negativeProfit]

def getTotalWalletVolumeAndTransfers(tx, walletAddress,):
    totalVolume = 0
    totalTransfersIn = 0
    totalTransfersOut = 0

    for transactions in tx:
        if (transactions['to'] == walletAddress.lower()):
            totalTransfersIn = totalTransfersIn + \
                float(transactions['value'])/ETHER_VALUE
        elif (transactions['from'] == walletAddress.lower()):
            totalTransfersOut = totalTransfersOut + \
                float(transactions['value'])/ETHER_VALUE
        totalVolume = totalVolume + float(transactions['value'])/ETHER_VALUE
    return totalVolume, totalTransfersIn, totalTransfersOut

def getTotalPositiveAndNegativeProfits(tokenList):
    positiveProfit = 0
    negativeProfit = 0
    for tokens in tokenList:
        profits = tokens[5]
        if (profits >= 0):
            positiveProfit = positiveProfit + profits
        else:
            negativeProfit = negativeProfit + profits
    return [positiveProfit, negativeProfit]

def getProfitHistoryOverview(tokenList, normalTransactions,walletAddress,ethUSD):
    totalTokensProfitable = 0
    profitTotal = 0
    totalTokensTraded = len(tokenList)
    if(totalTokensTraded == 0):
        totalTokensTraded = 1
    totalGas = calculateGasFees(normalTransactions,walletAddress) * ethUSD
    for tokens in tokenList:
        profitTotal = profitTotal + tokens[5]
        if(tokens[5] > 0):
            totalTokensProfitable = totalTokensProfitable + 1
    winRate = round((totalTokensProfitable/totalTokensTraded)*100,2)
    return [profitTotal,totalTokensTraded,totalTokensProfitable,winRate,totalGas]


def calculateGasFees(normalTransactions,walletAddress):
    totalGas = 0
    for transasctions in normalTransactions:
        if(transasctions['from'] == walletAddress.lower()):
            gasUsed = float(transasctions['gasUsed'])/ ETHER_VALUE
            gasPrice = float(transasctions['gasPrice']) 
            totalGas = totalGas + (gasUsed*gasPrice)
    return totalGas

def getTotalGasFees(transactions,walletAddress):
    totalGas = 0
    for transation in transactions:
        if(transation['from'] == walletAddress.lower()):
            gasUsed = float(transation['gasUsed'])/ ETHER_VALUE
            gasPrice = float(transation['gasPrice']) 
            totalGas = totalGas + (gasUsed*gasPrice)
    return totalGas

def getTokenImage(tokenName, tokenAmount):
    img_url = ""
    if(tokenAmount < 0 ):
        return img_url
    if(tokenName == "Toshi Tools"):
        img_url = "https://etherscan.io/token/images/toshitools_32.png"
    elif( tokenName == "Tether USD"):
        img_url = "https://assets.coingecko.com/coins/images/325/thumb/Tether.png?1668148663"
    elif( tokenName == "Optimus"):
        img_url = "https://assets.coingecko.com/coins/images/21678/thumb/rsz_logo%281%29.png?1639712718"
    elif(coinList.objects.filter(name=tokenName)):
        identity = coinList.objects.filter(name=tokenName).values()[0]['identification']   
        if(coinImages.objects.filter(identification = identity)):
            img_url = coinImages.objects.filter(identification = identity).values()[0].get("image_url")
        else:
            image_url = "https://api.coingecko.com/api/v3/coins/" + identity + "?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false"  + "&x_cg_pro_api_key=CG-o8B8B9FoSYrQEDAoFeGveNZU"
            response = get(image_url)
            data = response.json()
            if(data.get("image")):
                ci = coinImages(
                identification=identity, 
                image_url= data.get("image").get("thumb"), 
                )
                ci.save()
                img_url = data.get("image").get("thumb")
    return img_url

def completeDetailedTokens(detailedTokens,marketPriceAndTokenAllotment, ethUSD):
    completedTokens = []
    for tokens in detailedTokens:
        # GET THE TOKEN ARRAY
        tokenArray = detailedTokens.get(tokens)
        # print("*******************************")
        # print(tokenArray)
        # GET THE TOKEN ADDRESS
        tokenContractAddress = tokenArray[2]
        # GET THE MARKET PRICE AND TOKEN AMOUNT
        marketPriceAndTokenAmount = marketPriceAndTokenAllotment.get(tokenContractAddress)
        # ASSET AMOUNT
        assetAmount = marketPriceAndTokenAmount[1]
        # MARKET PRICE
        marketPrice = marketPriceAndTokenAmount[0]
        if(assetAmount != -1):
            tokenArray[4] = assetAmount
        img_url = getTokenImage(tokenArray[0],tokenArray[4])
        if(tokenArray[4] <= 0.0000000000000001):
            tokenArray[6] = 0
            tokenArray[7] = 0
        else:
            tokenArray[6] = tokenArray[4] * marketPrice * ethUSD
            tokenArray[7] = tokenArray[4] * marketPrice
            # if(tokenArray[2] == "0x529B6FfC8E5335181fe8397bc9F927e983D5c986"):
            #     print(marketPrice)
            #     print(tokenArray)
            if(tokenArray[2] == "0x243cACb4D5fF6814AD668C3e225246efA886AD5a"):
                tokenArray[6] = tokenArray[4] * (122.188068/110000000000) * ethUSD
                tokenArray[7] = tokenArray[4] * (122.188068/110000000000)
            elif(tokenArray[2] == "0xbb9FD9Fa4863C03c574007fF3370787B9cE65ff6"):
                tokenArray[6] = tokenArray[4] * (10.990033/1064908.65207743142) * ethUSD
                tokenArray[7] = tokenArray[4] * (10.990033/1064908.65207743142)
            elif(tokenArray[2] == "0x8A2D988Fe2E8c6716cbCeF1B33Df626C692F7B98"):
                tokenArray[6] = tokenArray[4] * 0 * ethUSD
                tokenArray[7] = tokenArray[4] * 0
            elif(tokenArray[2] == "0x0ab87046fBb341D058F17CBC4c1133F25a20a52f"):
                tokenArray[6] = tokenArray[4] * 2.09 * ethUSD
                tokenArray[7] = tokenArray[4] * 2.09
            elif(tokenArray[2] == "0xf34960d9d60be18cC1D5Afc1A6F012A723a28811"):
                tokenArray[6] = tokenArray[4] * 0.0060 * ethUSD
                tokenArray[7] = tokenArray[4] * 0.0060
        tokenArray[9] = img_url
        # print(tokenArray)
        # print("*******************************")
        completedTokens.append(tokenArray)
    return completedTokens

def getTokenDetailsAndProfit(erc20Transactions, normalTransactions, internalTransactions,walletAddress,ethUSD):
    tokenInfo = dict()
    transactionHistory = dict()
     # Iterate through all token transfer events
    for tokensTransfers in erc20Transactions:
        # Get Token Name
        tokenName = tokensTransfers.get('tokenName')
        # Get Token Symbol
        tokenSymbol = tokensTransfers.get('tokenSymbol')
        # Get Token Transaction Hash
        txHash = tokensTransfers.get("hash")
        # Get The From Address
        fromAddress = tokensTransfers.get('from')
        # Get The contract address
        contractAddress = getCheckSumWalletAddress(tokensTransfers.get('contractAddress'))
        # Get the token allocation
        tokenAllocation = float(tokensTransfers['value'])/(10 ** float(tokensTransfers['tokenDecimal']))
        # Record Transactions
        if(transactionHistory.get(txHash)):
            transactionHistory.update({
                txHash: transactionHistory.get(txHash) + 1
            })
        else:
            transactionHistory.update({
                txHash: 1
            })
        # If we are sending a transacation to another user (selling)
        if(fromAddress == walletAddress.lower()):
            price_change = 0
            token_profit = 0
            tokenAmount = 0
            if(internalTransactions.get(txHash)):
                if(not tokenBuyingPrice.get(contractAddress)):
                    tokenBuyingPrice.update({
                        contractAddress: 0
                })
                if(transactionHistory.get(txHash) > 1):
                    tokenAmount = 0
                else:
                    tokenAmount = internalTransactions.get(txHash)*ethUSD
            # else:
            #     print("THIS IS WHERE WE CHECK BLOCKCHAIN FOR SELL ORDERS")
            if (tokenInfo.get(tokenName)):
                token_profit = tokenInfo.get(tokenName)[5] + tokenAmount
                if(tokenInfo.get(tokenName)[5] == 0):
                    price_change = round(((tokenInfo.get(tokenName)[5] - tokenAmount)/1)*100,2)
                else:
                    price_change = round(((tokenInfo.get(tokenName)[5] - tokenAmount)/tokenInfo.get(tokenName)[5])*100,2)
                tokenInfo.update({
                    tokenName: [
                        tokenName, # Token Nam
                        tokenSymbol, # Token Symbol
                        contractAddress, # ContractAddress
                        tokenInfo.get(tokenName)[3] + 1, # Total Number of Transactions
                        tokenInfo.get(tokenName)[4] - tokenAllocation, # Current Holdings (Token)
                        token_profit, # Total Profit
                        0, # Current Holdings (USD)
                        0, # Current Holdings (ETH)
                        txHash, # transactionHash
                        "Coin_Image", # Coin Image
                        abs(price_change), # Profit Change
                        tokensTransfers['tokenDecimal'] # Token Decimal
                    ]
                })
            else:

                price_change = 100
                token_profit =  tokenAmount
                tokenInfo.update({
                    tokenName: [
                        tokenName, # Token Name
                        tokenSymbol, # Token Symbol
                        contractAddress, # ContractAddress
                        1, # Total Number of Transactions
                        0, # Current Holdings (Token)
                        token_profit, # Total Profit
                        0, # Current Holdings (USD)
                        0, # Current Holdings (ETH)
                        txHash, # transactionHash
                        "Coin_Image", # Coin Image
                        0, # Profit Change
                        tokensTransfers['tokenDecimal'] # Token Decimal
                    ]
                })
        # If we are recieving a transacation to another user (buying)
        else:
            purchaseAmount = 0
            if(normalTransactions.get(txHash)):
                tokenAmount = 0
                purchaseAmount = normalTransactions.get(txHash) * ethUSD
                if(tokenBuyingPrice.get(contractAddress)):
                    percentageChange = abs((tokenBuyingPrice.get(contractAddress) - tokenAmount)/tokenAmount)*100
                    if(percentageChange > 50 and tokenAmount != 0):
                        tokenBuyingPrice.update({
                            contractAddress: tokenAmount
                        })
                    else:
                        tokenBuyingPrice.update({
                            contractAddress: (tokenBuyingPrice.get(contractAddress) + tokenAmount)/2
                        })
                else:
                    tokenBuyingPrice.update({
                        contractAddress: tokenAmount
                    })
            else:
                tokenAmount = 0
                if(tokenBuyingPrice.get(contractAddress)):
                    tokenBuyingPrice.update({
                        contractAddress: (tokenBuyingPrice.get(contractAddress) + tokenAmount)/2
                    })
                else:
                    tokenBuyingPrice.update({
                        contractAddress: 0
                    })

            if (tokenInfo.get(tokenName)):
                tokenInfo.update({
                    tokenName: [
                        tokenName, # Token Name
                        tokenSymbol, # Token Symbol
                        contractAddress, # ContractAddress
                        tokenInfo.get(tokenName)[3] + 1, # Total Number of Transactions
                        tokenInfo.get(tokenName)[4]+ tokenAllocation, # Current Holdings (Token)
                        tokenInfo.get(tokenName)[5] - purchaseAmount, # Total Profit
                        tokenInfo.get(tokenName)[6], # Current Holdings (USD)
                        tokenInfo.get(tokenName)[7], # Current Holdings (ETH)
                        txHash, # transactionHash
                        "Coin_Image", # Coin Image
                        tokenInfo.get(tokenName)[10], # Profit Change
                        tokensTransfers['tokenDecimal'] # Token Decimal
                    ]
                })
            else:
                tokenInfo.update({
                    tokenName: [
                        tokenName, # Token Name
                        tokenSymbol, # Token Symbol
                        contractAddress, # ContractAddress
                        1, # Total Number of Transactions
                        tokenAllocation, # Current Holdings (Token)
                        -1* purchaseAmount, # Total Profit
                        0, # Current Holdings (USD)
                        0, # Current Holdings (ETH)
                        txHash, # transactionHash
                        "Coin_Image", # Coin Image
                        0, # Profit Change
                        tokensTransfers['tokenDecimal'] # Token Decimal
                    ]
                })
    return tokenInfo

def getCheckSumWalletAddress(nonCheckSumWalletAddress):
    return Web3.toChecksumAddress('0x' + str(nonCheckSumWalletAddress[-40:]))

def getMaxERC20Transactions(walletAddress):
    transactions_url = make_api_url(
        "account",
        "tokentx",
        walletAddress,
        startblock=0,
        endblock=99999999,
        page=1,
        offset=5000,
        sort="asc"
    )
    response = get(transactions_url)
    data = response.json()["result"]
    return data

def getMaxNormalTransactions(walletAddress):
    transactions_url = make_api_url(
        "account",
        "txlist",
        walletAddress,
        startblock=0,
        endblock=99999999,
        page=1,
        offset=5000,
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
        offset=5000,
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

def splitTimes(transactions):
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    dailyTransactions = []
    weeklyTransactions = []
    monthlyTransactions = []
    yearlyTransactions = []
    for transaction in transactions:
        timeDifference = currentDateAndTime - \
            float(transaction.get("timeStamp"))
        if (timeDifference < unix_day):
            dailyTransactions.append(transaction)
        if (timeDifference < unix_week):
            weeklyTransactions.append(transaction)
        if (timeDifference < unix_month):
            monthlyTransactions.append(transaction)
        if (timeDifference < unix_year):
            yearlyTransactions.append(transaction)
    return dailyTransactions, weeklyTransactions, monthlyTransactions, yearlyTransactions

def convertTransactionFromArrayToDict(transactions):
    txDict = dict()
    for tx in transactions:
        transactionHash = tx['hash']
        tokenAmount = float(tx["value"])/(ETHER_VALUE)
        txDict.update({
            transactionHash: tokenAmount,
        })
    return txDict

