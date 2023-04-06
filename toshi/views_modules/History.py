from ..views_modules import Misc
import json
from requests import get
from web3 import Web3, HTTPProvider
from ..models import coinList, coinImages
from datetime import datetime
import time
import requests
import ethers

FILE_NAME = 'HISTORY PAGE OVERVIEW '
DEBUG = True
BASE_URL = "https://api.etherscan.io/api"
API_KEY = "239PUCE9PMQCURRRZPVXRBESYPF4HUHRMZ"
ETHER_VALUE = 10 ** 18
web3eth = Web3(Web3.HTTPProvider(
    "https://mainnet.infura.io/v3/21a13d88d64f420d91ff5c3272c0f8b0"))

unix_day = 86400
unix_week = 604800
unix_month = 2628000
unix_year = 31540000

erc20TokenAbi = [{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"}]
uniswapAbi = [{"inputs": [],"name": "getReserves","outputs": [{"internalType": "uint112","name": "_reserve0","type": "uint112"},{"internalType": "uint112","name": "_reserve1","type": "uint112"},{"internalType": "uint32","name": "_blockTimestampLast","type": "uint32"}],"stateMutability": "view","type": "function"},{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]

def run(walletAddress):
    start_time = time.time()
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    # Convert wallet to checksum
    checkSumwalletAddress = getCheckSumWalletAddress(walletAddress)

    # Eth to USD conversion data
    Current_Eth_response = get(
        "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    Current_Eth_data = Current_Eth_response.json()
    ethUSD = float(Current_Eth_data.get("price"))
    yesterdayETHUSD = getYesterdayPriceChange()
    priceChange = round(((ethUSD - yesterdayETHUSD)/(ethUSD))*100,2)
    # Get Transactions using API call
    maxERC20Transactions = getMaxERC20Transactions(checkSumwalletAddress)
    maxNormalTransactions = getMaxNormalTransactions(checkSumwalletAddress)
    maxInternalTransactions = getMaxInternalTransactions(checkSumwalletAddress)

    # testWeb3Py(maxERC20Transactions)
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

    # Get profit at each time frame
    maxProfitArray = getTotalTokenProfits(maxDictNormalTransactions, maxDictInternalTransactions, maxERC20Transactions, checkSumwalletAddress)
    yearlyProfitArray = getTotalTokenProfits(yearlyDictNormalTransactions, yearlyDictInternalTransactions, yearlyERC20Transactions, checkSumwalletAddress)
    monthlyProfitArray = getTotalTokenProfits(monthlyDictNormalTransactions, monthlyDictInternalTransactions, monthlyERC20Transactions, checkSumwalletAddress)
    weeklyProfitArray = getTotalTokenProfits(weeklyDictNormalTransactions, weeklyDictInternalTransactions, weeklyERC20Transactions, checkSumwalletAddress)
    dailyProfitArray = getTotalTokenProfits(dailyDictNormalTransactions, dailyDictInternalTransactions, dailyERC20Transactions, checkSumwalletAddress)

    maxProfit = maxProfitArray[0]
    yearlyProfit = yearlyProfitArray[0]
    monthlyProfit = monthlyProfitArray[0]
    weeklyProfit = weeklyProfitArray[0]
    dailyProfit = dailyProfitArray[0]
    # Get wallet volume and transfers per time frame
    maxWalletVolumeAndTransfers = getTotalWalletVolumeAndTransfers(maxNormalTransactions, checkSumwalletAddress)
    yearlyWalletVolumeAndTransfers = getTotalWalletVolumeAndTransfers(yearlyInternalTransactions, checkSumwalletAddress)
    monthlyWalletVolumeAndTransfers = getTotalWalletVolumeAndTransfers(monthlyInternalTransactions, checkSumwalletAddress)
    weeklyWalletVolumeAndTransfers = getTotalWalletVolumeAndTransfers(weeklyInternalTransactions, checkSumwalletAddress)
    dailyWalletVolumeAndTransfers = getTotalWalletVolumeAndTransfers(dailyInternalTransactions, checkSumwalletAddress)

    # Get Total Profit and Negative per time frame
    maxTotalProfit = getTotalPositiveAndNegativeProfits(maxProfit)
    yearlyTotalProfit = getTotalPositiveAndNegativeProfits(yearlyProfit)
    monthlyTotalProfit = getTotalPositiveAndNegativeProfits(monthlyProfit)
    weeklyTotalProfit = getTotalPositiveAndNegativeProfits(weeklyProfit)
    dailyTotalProfit = getTotalPositiveAndNegativeProfits(dailyProfit)

    # Create the max volume overview data per timeframe
    maxVolumeHistoryOverview = [
        maxWalletVolumeAndTransfers[0] * ethUSD,
        maxWalletVolumeAndTransfers[1] * ethUSD,
        maxWalletVolumeAndTransfers[2] * ethUSD,
        maxTotalProfit[0] * ethUSD,
        maxTotalProfit[1] * ethUSD
    ]

    yearlyVolumeHistoryOverview = [
        yearlyWalletVolumeAndTransfers[0] * ethUSD,
        yearlyWalletVolumeAndTransfers[1] * ethUSD,
        yearlyWalletVolumeAndTransfers[2] * ethUSD,
        yearlyTotalProfit[0] * ethUSD,
        yearlyTotalProfit[1] * ethUSD
    ]
    monthlyVolumeHistoryOverview = [
        monthlyWalletVolumeAndTransfers[0] * ethUSD,
        monthlyWalletVolumeAndTransfers[1] * ethUSD,
        monthlyWalletVolumeAndTransfers[2] * ethUSD,
        monthlyTotalProfit[0] * ethUSD,
        monthlyTotalProfit[1] * ethUSD
    ]
    weeklyVolumeHistoryOverview = [
        weeklyWalletVolumeAndTransfers[0] * ethUSD,
        weeklyWalletVolumeAndTransfers[1] * ethUSD,
        weeklyWalletVolumeAndTransfers[2] * ethUSD,
        weeklyTotalProfit[0] * ethUSD,
        weeklyTotalProfit[1] * ethUSD
    ]
    dailyVolumeHistoryOverview = [
        dailyWalletVolumeAndTransfers[0] * ethUSD,
        dailyWalletVolumeAndTransfers[1] * ethUSD,
        dailyWalletVolumeAndTransfers[2] * ethUSD,
        dailyTotalProfit[0] * ethUSD,
        dailyTotalProfit[1] * ethUSD
    ]

    # VOLUME HISTORY OVERVIEW DATA, CONTAINS VOLUME HISTORY DATA FOR EACH TIME FRAME IN THE FOLLOWING ORDER:
    # DAILY, WEEKLY, MONTHLY, YEARLY, MAX
    volumeHistoryOverview = [
        dailyVolumeHistoryOverview,
        weeklyVolumeHistoryOverview,
        monthlyVolumeHistoryOverview,
        yearlyVolumeHistoryOverview,
        maxVolumeHistoryOverview
    ]

    # GET TOTAL SUM PROFIT 
    maxSumTotal = maxTotalProfit[0] + maxTotalProfit[1]
    yearlySumTotal = yearlyTotalProfit[0] + yearlyTotalProfit[1]
    monthlySumTotal = monthlyTotalProfit[0] + monthlyTotalProfit[1]
    weeklySumTotal = weeklyTotalProfit[0] + weeklyTotalProfit[1]
    dailySumTotal = dailyTotalProfit[0] + dailyTotalProfit[1]

    # GET TOTAL TOKENS TRADED
    maxtotalTokenTraded = len(getTotalTokensTraded(maxERC20Transactions))
    yearlytotalTokenTraded = len(getTotalTokensTraded(yearlyERC20Transactions))
    monthlytotalTokenTraded = len(getTotalTokensTraded(monthlyERC20Transactions))
    weeklytotalTokenTraded = len(getTotalTokensTraded(weeklyERC20Transactions))
    dailytotalTokenTraded = len(getTotalTokensTraded(dailyERC20Transactions))

    if(maxtotalTokenTraded == 0):
        maxtotalTokenTraded = 1
    if(yearlytotalTokenTraded == 0):
        yearlytotalTokenTraded = 1
    if(monthlytotalTokenTraded == 0):
        monthlytotalTokenTraded = 1
    if(weeklytotalTokenTraded == 0):
        weeklytotalTokenTraded = 1
    if(dailytotalTokenTraded == 0):
        dailytotalTokenTraded = 1
    

    # Get Total Tokens Profitable
    maxTotalTokensProfitable = (getTotalTokensProfitable(maxProfit))
    yearlyTotalTokensProfitable = (getTotalTokensProfitable(yearlyProfit))
    monthlyTotalTokensProfitable = (getTotalTokensProfitable(monthlyProfit))
    weeklyTotalTokensProfitable = (getTotalTokensProfitable(weeklyProfit))
    dailtTotalTokensProfitable = (getTotalTokensProfitable(dailyProfit))

    # Get Win Rate
    maxWinRate = round((maxTotalTokensProfitable/maxtotalTokenTraded) * 100)
    yearlyWinRate = round((maxTotalTokensProfitable/maxtotalTokenTraded) * 100)
    monthlyWinRate = round((maxTotalTokensProfitable/maxtotalTokenTraded) * 100)
    weeklyWinRate = round((maxTotalTokensProfitable/maxtotalTokenTraded) * 100)
    dailyWinRate = round((maxTotalTokensProfitable/maxtotalTokenTraded) * 100)

    # Get Total Gas Fees Spent
    
    maxTotalGasFees = (getTotalGasFees(maxNormalTransactions, checkSumwalletAddress))
    yearlyTotalGasFees = (getTotalGasFees(yearlyNormalTransactions, checkSumwalletAddress))
    monthlyTotalGasFees = (getTotalGasFees(monthlyNormalTransactions, checkSumwalletAddress))
    weeklyTotalGasFees = (getTotalGasFees(weeklyNormalTransactions, checkSumwalletAddress))
    dailyTotalGasFees = (getTotalGasFees(dailyNormalTransactions, checkSumwalletAddress))

    # PROFIT HISTORY OVERVIEW DATA, CONTAINS PROFIT HISTORY DATA FOR EACH TIME FRAME IN THE FOLLOWING ORDER:
    # DAILY, WEEKLY, MONTHLY, YEARLY, MAX
    profitHistoryOverview = [
        [dailySumTotal * ethUSD,dailytotalTokenTraded,dailtTotalTokensProfitable,dailyWinRate,dailyTotalGasFees * ethUSD ],
        [weeklySumTotal * ethUSD,weeklytotalTokenTraded,weeklyTotalTokensProfitable,weeklyWinRate,weeklyTotalGasFees * ethUSD ],
        [monthlySumTotal * ethUSD,monthlytotalTokenTraded,monthlyTotalTokensProfitable,monthlyWinRate,monthlyTotalGasFees * ethUSD ],
        [yearlySumTotal * ethUSD,yearlytotalTokenTraded,yearlyTotalTokensProfitable,yearlyWinRate,yearlyTotalGasFees * ethUSD ],
        [maxSumTotal * ethUSD,maxtotalTokenTraded,maxTotalTokensProfitable,maxWinRate,maxTotalGasFees * ethUSD ]
    ]

    ### BEGIN CALCULATION FOR Token History Overview Table ###

    # GET TOKEN NAME, SYMBOL, CURRENT HOLDINGS, CONTRACT ADDRESS, AND NUMBER OF TRANSACITONS
    dailyTokenDetails = getTokenDetails(dailyERC20Transactions)
    weeklyTokenDetails = getTokenDetails(weeklyERC20Transactions)
    monthlyTokenDetails = getTokenDetails(monthlyERC20Transactions)
    yearlyTokenDetails = getTokenDetails(yearlyERC20Transactions)
    maxTokenDetails = getTokenDetails(maxERC20Transactions)

    # Add Token Holdings
    maxTokenDetailsWithAssetAllocation = getAssetAmmount(maxTokenDetails, checkSumwalletAddress)
    yearlyTokenDetailsWithAssetAllocation = getAssetAmmount(yearlyTokenDetails, checkSumwalletAddress)
    monthlyTokenDetailsWithAssetAllocation = getAssetAmmount(monthlyTokenDetails, checkSumwalletAddress)
    weeklyTokenDetailsWithAssetAllocation = getAssetAmmount(weeklyTokenDetails, checkSumwalletAddress)
    dailyTokenDetailsWithAssetAllocation = getAssetAmmount(dailyTokenDetails, checkSumwalletAddress)

    # ADD TOKEN PROFIT AND GET HOLDINGS IN ETH AND USD 
    # Array is in the following order
    #  (Token Name, Token Symbol, Contract Address, transactions, Current Holdings in native currency,
    # Current Holdings in usd, Current Holdings in eth, image url )

    maxTokenHistoryOverview = addProfitEthAndUSD(maxTokenDetailsWithAssetAllocation, maxProfit,ethUSD,maxProfitArray[1])
    yearlyTokenHistoryOverview = addProfitEthAndUSD(yearlyTokenDetailsWithAssetAllocation, yearlyProfit,ethUSD,yearlyProfitArray[1])
    monthlyTokenHistoryOverview = addProfitEthAndUSD(monthlyTokenDetailsWithAssetAllocation, monthlyProfit,ethUSD,monthlyProfitArray[1])
    weeklyTokenHistoryOverview = addProfitEthAndUSD(weeklyTokenDetailsWithAssetAllocation, weeklyProfit,ethUSD,weeklyProfitArray[1])
    dailyTokenHistoryOverview = addProfitEthAndUSD(dailyTokenDetailsWithAssetAllocation, dailyProfit,ethUSD,dailyProfitArray[1])

    # Token History Overview DATA, CONTAINS PROFIT HISTORY DATA FOR EACH TIME FRAME IN THE FOLLOWING ORDER:
    # DAILY, WEEKLY, MONTHLY, YEARLY, MAX
    tokenHistoryOverview = [
        dailyTokenHistoryOverview,
        weeklyTokenHistoryOverview,
        monthlyTokenHistoryOverview,
        yearlyTokenHistoryOverview,
        maxTokenHistoryOverview
    ]

    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
    print("--- %s seconds ---" % (time.time() - start_time))
    return [profitHistoryOverview, volumeHistoryOverview,tokenHistoryOverview]

def getAssetAmmount(assets,walletAddress):
    refinedAssets = assets
    for asset in refinedAssets:
        # Get an array of asset details of each asset
        assetArray = refinedAssets.get(asset)
        # Set the addresses of the token, exchange contracts, Eth, and USD
        tokenAddress = assetArray [2]
        # Get the contract instances for the token and exchange
        token = web3eth.eth.contract(address=tokenAddress, abi=json.loads(json.dumps(erc20TokenAbi))) # declaring the token contract
        # Get the token balance in wei
        rawBalance = token.functions.balanceOf(walletAddress).call()
        # Get the token decimal
        token_decimals = token.functions.decimals().call()      
        # Get balance in token amount
        balance = rawBalance / (10 ** token_decimals)
        # Replace old token amount with new token amount
        assetArray[4] = balance
    return refinedAssets

def getMarketPrice(token_address):
    # Set the addresses of the token, exchange contracts, Eth, and USD
    uniswap_exchange_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D' # Uniswap router v2 contract address
    eth_contract_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' # wEth contract address
    usd_contract_address = '0xdAC17F958D2ee523a2206206994597C13D831ec7' # tether contract address

    # Get the contract instances for the token and exchange
    token_contract = web3eth.eth.contract(address=token_address, abi=(json.dumps(erc20TokenAbi)))
    exchange_contract = web3eth.eth.contract(address=uniswap_exchange_address, abi=(json.dumps(uniswapAbi)))

    # Get the token decimal
    token_decimals = token_contract.functions.decimals().call()
    exchange_decimal = 18
    usd_decimal = 6

    # Set the input ammount
    token_input_amount = (10**token_decimals)
    exchange_input_amount = 1 * (10**exchange_decimal)

    # Set Path
    token_path = [token_address, eth_contract_address] # TOKEN -> ETH
    exchange_path = [eth_contract_address, usd_contract_address] # ETH -> USDC

    # Get the token exchange rates
    token_to_eth_price_wei = exchange_contract.functions.getAmountsOut(token_input_amount, token_path).call()
    eth_to_usd_price_wei = exchange_contract.functions.getAmountsOut(exchange_input_amount, exchange_path).call()

    # Get the token exhange rates in the proper units
    token_to_eth_price_eth = token_to_eth_price_wei[1]/(10**exchange_decimal)
    eth_to_usd_price_usd = eth_to_usd_price_wei[1]/(10**usd_decimal)

    # Get current market price of token in USD
    token_market_price = token_to_eth_price_eth * eth_to_usd_price_usd

    return token_market_price

def getYesterdayPriceChange():
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    yesterday = currentDateAndTime - unix_day - unix_day
    yesterdayFormat = coinGeckounixTimeStampToDateTime(yesterday)
    request_url = "https://api.coingecko.com/api/v3/coins/ethereum/history?date=" + yesterdayFormat + "&localization=false&x_cg_pro_api_key=CG-o8B8B9FoSYrQEDAoFeGveNZU"
    response = get(request_url)
    data = response.json()
    if(data.get("market_data")):
        return (data.get("market_data").get("current_price").get("usd"))
    return 1

def coinGeckounixTimeStampToDateTime(unix):
    return (
        datetime.fromtimestamp(
            int(unix)
        ).strftime('%d-%m-%Y')
    )

def addProfitEthAndUSD(tokenDetails, profits, ethToUSD,priceChange):
    tokenArrayToReturn = []
    for token in tokenDetails:

        img_url = ""
        # Make Token Array
        tokenArray = tokenDetails.get(token)
        # Get Token Address
        tokenAddress = tokenArray[2]
        # Get Token USD and Eth Values
        usdHolding = getMarketPrice(tokenAddress)
        usdHolding = usdHolding * tokenArray[4]
        if(tokenArray[4] < 0 ):
            continue
        if(tokenArray[0]== "Toshi Tools"):
            img_url = "https://etherscan.io/token/images/toshitools_32.png"
        elif(tokenArray[0]== "Tether USD"):
            img_url = "https://assets.coingecko.com/coins/images/325/thumb/Tether.png?1668148663"
        elif(tokenArray[0]== "Optimus"):
            img_url = "https://assets.coingecko.com/coins/images/21678/thumb/rsz_logo%281%29.png?1639712718"
        elif(coinList.objects.filter(name=tokenArray[0])):
            identity = coinList.objects.filter(name=tokenArray[0]).values()[0]['identification']   
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
        elif(coinList.objects.filter(symbol=tokenArray[1])):
            identity = coinList.objects.filter(symbol=tokenArray[1]).values()[0]['identification']   
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
        if(profits.get(token)):
            tokenArray.append(profits.get(token) * ethToUSD)
        else:
            tokenArray.append(0)
        tokenArray.append(usdHolding)
        ethHolding = usdHolding / ethToUSD
        tokenArray.append(ethHolding)
        tokenArray.append(img_url)
        if(priceChange.get(token)):
            tokenArray.append(priceChange.get(token))
        else:
            tokenArray.append(0)
        tokenArrayToReturn.append(tokenArray)
    return tokenArrayToReturn

def getTokenDetails(erc20Transactions):
    tokenInfo = dict()
    for tokens in erc20Transactions:
        tokenName = tokens['tokenName']
        tokenSymbol = tokens['tokenSymbol']
        contractAddress = getCheckSumWalletAddress(tokens['contractAddress'])
        if(tokenInfo.get(tokens['tokenName'])):
            tokenInfo.update({
                tokenName: [
                    tokenName, # Token Name
                    tokenSymbol, # Token Symbol
                    contractAddress, # ContractAddress
                    tokenInfo.get(tokens['tokenName'])[3] + 1, # Total Transactions
                    0, # Current Holdings
                ]
            })
        else:
            tokenInfo.update({
                tokenName: [
                    tokenName, # Token Name
                    tokenSymbol, # Token Symbol
                    contractAddress, # ContractAddress
                    1, # Total Transactions
                    0, # Current Holdings
                ]
            })
    return tokenInfo

def getTotalGasFees(transactions,walletAddress):
    totalGas = 0
    for transation in transactions:
        if(transation['from'] == walletAddress.lower()):
            gasUsed = float(transation['gasUsed'])/ ETHER_VALUE
            gasPrice = float(transation['gasPrice']) 
            totalGas = totalGas + (gasUsed*gasPrice)
    return totalGas
            
def getTotalTokensProfitable(profit):
    counter = 0
    for tokens in profit:
        if(profit.get(tokens) > 0):
            counter = counter + 1
    return counter

def getTotalTokensTraded(transactions):
    tokenCount = dict()
    for transaction in transactions:
        tokenName = transaction['tokenName']
        tokenCount.update({
            tokenName: 1,
        })
    return tokenCount

def getMaxERC20Transactions(walletAddress):
    transactions_url = make_api_url(
        "account",
        "tokentx",
        walletAddress,
        startblock=0,
        endblock=99999999,
        page=1,
        offset=1000,
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
        offset=1000,
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
        offset=1000,
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

def getTotalPositiveAndNegativeProfits(profitDict):
    positiveProfit = 0
    negativeProfit = 0
    for key in profitDict:
        profits = profitDict.get(key)
        if (profits >= 0):
            positiveProfit = positiveProfit + profits
        else:
            negativeProfit = negativeProfit + profits
    return [positiveProfit, negativeProfit]

def getTotalWalletVolumeAndTransfers(tx, walletAddress):
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
    return [totalVolume, totalTransfersIn, totalTransfersOut]

def convertTransactionFromArrayToDict(transactions):
    txDict = dict()
    for tx in transactions:
        transactionHash = tx['hash']
        tokenAmount = float(tx["value"])/(ETHER_VALUE)
        txDict.update({
            transactionHash: tokenAmount,
        })
    return txDict

def getTotalTokenProfits(dictNormalTransactions, dictInternalTransactions, erc20Transactions, checkSumwalletAddress):
    tokenInfo = dict()
    tokenProfit = dict()
    tokenPriceChange = dict()
    # Iterate through all token transfer events
    for tokensTransfers in erc20Transactions:
        tokenAllocation = float(tokensTransfers['value'])/(10 ** float(tokensTransfers['tokenDecimal']))
        # Get Token Symbol
        tokenSymbol = tokensTransfers['tokenName']
        # Get The Transaction Hash
        txHash = tokensTransfers['hash']
        # If the token is in our list
        if (tokenInfo.get(tokenSymbol)):
            # If the token is going to the user
            if (tokensTransfers['to'] == checkSumwalletAddress.lower()):
                # Get Token Value if it exists
                if (dictNormalTransactions.get(txHash)):
                    tokenAmount = dictNormalTransactions[txHash] / tokenAllocation
                    tokenInfo.update({
                        tokenSymbol: (tokenInfo.get(tokenSymbol) + tokenAmount)/2
                    })
                elif (coinList.objects.filter(name=tokensTransfers['tokenName'])):
                    historicalDate = coinGeckounixTimeStampToDateTime(
                        tokensTransfers['timeStamp'])
                    identification = coinList.objects.filter(
                        name=tokensTransfers['tokenName']).values()[0]['identification']
                    if (getPastPriceCrypto(identification, historicalDate).get("market_data")):
                        tokenEthPrice = getPastPriceCrypto(identification, historicalDate).get(
                            "market_data").get("current_price").get("eth")
                        tokenInfo.update({
                            tokenSymbol: (tokenInfo.get(tokenSymbol) + tokenEthPrice)/2
                        })
            # If the token is leaving the user, This is where we calculate profit
            elif (tokensTransfers['from'] == checkSumwalletAddress.lower()):
                # Get Token Value if it exists
                if (dictInternalTransactions.get(txHash)):
                    tokenAmount = dictInternalTransactions[txHash]
                    price_change = (round(((tokenAmount - (tokenInfo.get(tokenSymbol) * tokenAllocation))/(tokenAmount))*100),2)
                    tokenPriceChange.update({
                        tokenSymbol: price_change
                    })
                    if (tokenProfit.get(tokenSymbol)):
                        tokenProfit.update({
                            tokenSymbol: tokenProfit.get(tokenSymbol) + (tokenAmount - (tokenInfo.get(tokenSymbol) * tokenAllocation))
                        })
                    else:
                        tokenProfit.update({
                            tokenSymbol: tokenAmount -(tokenInfo.get(tokenSymbol) * tokenAllocation)
                        })
                elif (coinList.objects.filter(name=tokensTransfers['tokenName'])):
                    tokenAmount = 0
                    historicalDate = coinGeckounixTimeStampToDateTime(
                        tokensTransfers['timeStamp'])
                    identification = coinList.objects.filter(
                        name=tokensTransfers['tokenName']).values()[0]['identification']
                    if (getPastPriceCrypto(identification, historicalDate).get("market_data")):
                        tokenEthPrice = getPastPriceCrypto(identification, historicalDate).get(
                            "market_data").get("current_price").get("eth")
                        if (tokenProfit.get(tokenSymbol)):
                            tokenProfit.update({
                                tokenSymbol: tokenProfit.get(
                                    tokenSymbol) + (tokenAmount - (tokenEthPrice * tokenAllocation))
                            })
                        else:
                            tokenProfit.update({
                                tokenSymbol: tokenAmount -(tokenEthPrice * tokenAllocation)
                            })
        # If the token is not in our list
        else:
            # Get Token Value if it exists
            if (dictNormalTransactions.get(txHash)):
                tokenAmount = dictNormalTransactions[txHash]
                if(tokenAllocation > 0):
                    tokenAmount = dictNormalTransactions[txHash] / tokenAllocation
                # If the token is going to the user
                if (tokensTransfers['to'] == checkSumwalletAddress.lower()):
                    tokenInfo.update({
                        tokenSymbol: tokenAmount
                    })
            # If the token does not exist, we check coingecko
            else:
                # If the token is going to the user
                if (tokensTransfers['to'] == checkSumwalletAddress.lower()):
                    if (tokensTransfers['tokenName'] == "Tether USD"):
                        tokenInfo.update({
                            tokenSymbol: tokenAllocation
                        })
                    elif (coinList.objects.filter(name=tokensTransfers['tokenName'])):
                        historicalDate = coinGeckounixTimeStampToDateTime(
                            tokensTransfers['timeStamp'])
                        identification = coinList.objects.filter(
                            name=tokensTransfers['tokenName']).values()[0]['identification']
                        if (getPastPriceCrypto(identification, historicalDate).get("market_data")):
                            tokenEthPrice = getPastPriceCrypto(identification, historicalDate).get(
                                "market_data").get("current_price").get("eth")
                            tokenInfo.update({
                                tokenSymbol: tokenEthPrice
                            })
    return [tokenProfit,tokenPriceChange]

def coinGeckounixTimeStampToDateTime(unix):
    return (
        datetime.fromtimestamp(
            int(unix)
        ).strftime('%d-%m-%Y')
    )

def getPastPriceCrypto(identification, date):
    url = "https://pro-api.coingecko.com/api/v3/coins/" + identification + "/history?date=" + \
        date + "&localization=false" + "&x_cg_pro_api_key=CG-o8B8B9FoSYrQEDAoFeGveNZU"
    response = get(url)
    data = response.json()
    return data

def getCheckSumWalletAddress(nonCheckSumWalletAddress):
    return Web3.toChecksumAddress('0x' + str(nonCheckSumWalletAddress[-40:]))