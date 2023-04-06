from ..receive import Misc
import json
from requests import get
from web3 import Web3
from ...models import coinList, coinImages
from datetime import datetime
import time
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor

# CONSTANTS
FILE_NAME = 'HISTORY PAGE OVERVIEW '
DEBUG = True
BASE_URL = "https://api.etherscan.io/api"
API_KEY = "239PUCE9PMQCURRRZPVXRBESYPF4HUHRMZ"
ETHER_VALUE = 10 ** 18
NUM_RETRIES = 30
RETRY_DELAY = 1.2
GLOBAL_WALLET_ADDRESS = ""

# API LINKS
web3ethAlchemy = Web3(Web3.HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/_mEa4ksrzCdb8fgB5_7-4doIZrMWwpKf"))
# web3ethInfura= Web3(Web3.HTTPProvider(" https://mainnet.infura.io/v3/21a13d88d64f420d91ff5c3272c0f8b0"))


# TIMESTAMPS
unix_day = 86400
unix_week = 604800
unix_month = 2628000
unix_year = 31540000

# ABI
erc20TokenAbi = [{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"payable":True,"stateMutability":"payable","type":"fallback"},{"anonymous":False,"inputs":[{"indexed":True,"name":"owner","type":"address"},{"indexed":True,"name":"spender","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]
uniswapAbi = [{"inputs": [],"name": "getReserves","outputs": [{"internalType": "uint112","name": "_reserve0","type": "uint112"},{"internalType": "uint112","name": "_reserve1","type": "uint112"},{"internalType": "uint32","name": "_blockTimestampLast","type": "uint32"}],"stateMutability": "view","type": "function"},{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
uniswap_v3_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]')

# ASSET AMOUNT, MARKET PRICE, TOKEN PURCHASE PRICE
tokenBuyingPrice = dict()
priceAndAsset = dict()
completedTokenList = [[],[],[],[],[]]

def getCheckSumWalletAddress(nonCheckSumWalletAddress):
    return Web3.toChecksumAddress('0x' + str(nonCheckSumWalletAddress[-40:]))

def make_api_url(module, action, wallet_address, **kwargs):
    url = BASE_URL + \
        f"?module={module}&action={action}&address={wallet_address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url


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

def splitTimes(transactions):
    currentDateAndTime = time.mktime(datetime.now().timetuple())
    dailyTransactions = []
    weeklyTransactions = []
    monthlyTransactions = []
    yearlyTransactions = []
    for transaction in transactions:
        timeDifference = currentDateAndTime - float(transaction['timeStamp'])
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

def getTokenDetailsAndProfit(erc20Transactions, normalTransactions, internalTransactions,walletAddress,ethUSD,transfersList):
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
                        tokensTransfers['tokenDecimal'], # Token Decimal
                        transfersList.get(tokenName)[0], # Transfer In,
                        transfersList.get(tokenName)[1], # Transfer Out,
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
                        tokensTransfers['tokenDecimal'], # Token Decimal
                        transfersList.get(tokenName)[0], # Transfer In,
                        transfersList.get(tokenName)[1], # Transfer Out,
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
                        tokensTransfers['tokenDecimal'], # Token Decimal
                        transfersList.get(tokenName)[0], # Transfer In,
                        transfersList.get(tokenName)[1], # Transfer Out,
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
                        tokensTransfers['tokenDecimal'], # Token Decimal,
                        transfersList.get(tokenName)[0], # Transfer In,
                        transfersList.get(tokenName)[1], # Transfer Out,
                    ]
                })
    return tokenInfo

def sortTokenDetailsAndProfit(tokensAndProfitList):
    sorted_dict = {k: v for k, v in sorted(tokensAndProfitList.items(), key=lambda item: item[1][5], reverse=True )}
    return sorted_dict

def getMarketPriceAssetAllocation(tokenAddressAndDecimal,walletAddress):
    # Set the addresses of the token, exchange contracts, Eth, and USD
    uniswap_exchange_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D' # Uniswap router v2 contract address
    eth_contract_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' # wEth contract address
    tokenAddress = tokenAddressAndDecimal[0]
    rawBalance = 0
    balance = 0
    # IF WE ALREADY HAVE THE PRICE NO NEED TO LOOK FOR IT AGAIN
    if(priceAndAsset.get(tokenAddress)):
        return priceAndAsset

    # IF THE ASSET IS ETHEREUM
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

    try:
        # Get the token balance in wei
        rawBalance = token.functions.balanceOf(walletAddress).call()
    except:
        print("BALANCE EXCEPTION")
        # If there's an error, retry the API call
        for i in range(NUM_RETRIES):
            # print(f"Retrying API call in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
            try:
                # Get the token balance in wei
                rawBalance = token.functions.balanceOf(walletAddress).call()
            except:
                print("BALANCE RETRY")

    # Get balance in token amount
    balance = rawBalance / (10 ** token_decimals)
    print("|||||||||||||||||||||||||||||||||||||||||||||||||")
    print("TOKEN ADDRESS: ", tokenAddress)
    print("RAW BALANCE: ", rawBalance)
    print("BALANCE: ", balance)
    print("|||||||||||||||||||||||||||||||||||||||||||||||||")
    if(balance == 0):
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
            token_to_eth_price_wei[1] = (getTransactionEthFromBlockchain(tokenAddress))

    # Get the token exhange rates in the proper units
    token_to_eth_price_eth = token_to_eth_price_wei[1]/((10**exchange_decimal))

    priceAndAsset.update({
        tokenAddress : [
            balance,token_to_eth_price_eth
        ]
    })
    return priceAndAsset

def getTransactionEthFromBlockchain(token_address):
    # Get the contract instances for the token
    token = web3ethAlchemy.eth.contract(address=token_address, abi=json.loads(json.dumps(erc20TokenAbi))) # declaring the token contract
    # Get the token decimal
    exchange_decimal = 18
    latest_block = web3ethAlchemy.eth.block_number
    event_filter = token.events.Transfer.createFilter(fromBlock=0)
    events = event_filter.get_all_entries()
    before = 0
    after = 0
    if len(events) > 0:
        most_recent_event = events[-1]
        tx_hash = most_recent_event['transactionHash'].hex()
        block_number = web3ethAlchemy.eth.getTransaction(tx_hash).blockNumber
        from_user = most_recent_event['args']['from']
        try:
            before = web3ethAlchemy.eth.get_balance(from_user, block_number-1)
            after = web3ethAlchemy.eth.get_balance(from_user, block_number+1)
        except:
            # If there's an error, retry the API call
            for i in range(NUM_RETRIES):
                time.sleep(RETRY_DELAY)
                try:
                    before = web3ethAlchemy.eth.get_balance(from_user, block_number-1)
                    after = web3ethAlchemy.eth.get_balance(from_user, block_number+1)
                except:
                    print("retry blockchain search")
    return ((abs(after - before))/(10 ** exchange_decimal))

def calculateGasFees(normalTransactions,walletAddress):
    totalGas = 0
    for transasctions in normalTransactions:
        if(transasctions['from'] == walletAddress.lower()):
            gasUsed = float(transasctions['gasUsed'])/ ETHER_VALUE
            gasPrice = float(transasctions['gasPrice']) 
            totalGas = totalGas + (gasUsed*gasPrice)
    return totalGas

def getProfitHistoryOverview(tokenList, normalTransactions,walletAddress,ethUSD):
    totalTokensProfitable = 0
    profitTotal = 0
    totalTokensTraded = len(tokenList)
    if(totalTokensTraded == 0):
        totalTokensTraded = 1
    totalGas = calculateGasFees(normalTransactions,walletAddress) * ethUSD
    for tokens in tokenList:
        tokenArray = tokenList.get(tokens)
        profitTotal = profitTotal + tokenArray[5]
        if(tokenArray[5] > 0):
            totalTokensProfitable = totalTokensProfitable + 1
    winRate = round((totalTokensProfitable/totalTokensTraded)*100,2)
    return [profitTotal,totalTokensTraded,totalTokensProfitable,winRate,totalGas]


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
        tokenArray = tokenList.get(tokens)
        profits = tokenArray[5]
        if (profits >= 0):
            positiveProfit = positiveProfit + profits
        else:
            negativeProfit = negativeProfit + profits
    return [positiveProfit, negativeProfit]

def getVolumeHistoryOverview(maxDetailedTokens,maxNormalTransactions,checksumWalletAddress,ethUSD):
    totalVolume, totalTransfersIn, totalTransfersOut = getTotalWalletVolumeAndTransfers(maxNormalTransactions,checksumWalletAddress)
    positiveProfit,negativeProfit = getTotalPositiveAndNegativeProfits(maxDetailedTokens)
    return [totalVolume*ethUSD,totalTransfersIn*ethUSD,totalTransfersOut*ethUSD,positiveProfit,negativeProfit]

def TokenAllotmentAndMarketPrice(tokenList,walletAddress,ethUSD,self,ProfitHistoryOverviewAndVolumeHistoryOverview,timeFrame):
    contractAddressList = []
    global completedTokenList
    for tokens in tokenList:
        tokenArray = tokenList.get(tokens)
        # TOKEN NAME
        tokenName = tokenArray[0]
        # TOKEN AMOUNT
        tokenAmount = tokenArray[4]
        tokenDecimal = tokenArray[11]
        contractAddress = tokenArray[2]
        contractAddressList.append([contractAddress,tokenDecimal,tokenAmount,tokenName])
    # print("************************************")
    # print(tokenList)
    # print("************************************")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        assetsAndMarketPrice = {executor.submit(getMarketPriceAssetAllocation, contractAddressList, walletAddress): contractAddressList for contractAddressList in contractAddressList}
        for future in concurrent.futures.as_completed(assetsAndMarketPrice):
            assetAndPrice = assetsAndMarketPrice[future]
            if(not future.exception()):
                data = future.result()
                marketPrice = data.get(assetAndPrice[0])[1]
                holdingsAmount = data.get(assetAndPrice[0])[0]
                tokenArrayReturned = tokenList.get(assetAndPrice[3])
                returnedArray = completeDetailedTokens(tokenArrayReturned,marketPrice,holdingsAmount,ethUSD,self)
                if(timeFrame == "daily"):
                    completedTokenList[0].append(returnedArray)
                elif(timeFrame == "weekly"):
                    completedTokenList[1].append(returnedArray)
                elif(timeFrame == "monthly"):
                    completedTokenList[2].append(returnedArray)
                elif(timeFrame == "yearly"):
                    completedTokenList[3].append(returnedArray)
                elif(timeFrame == "max"):
                    if(returnedArray not in completedTokenList[4]):
                        completedTokenList[4].append(returnedArray)
                websocketHistoryResponse = {
                    'response' : [ProfitHistoryOverviewAndVolumeHistoryOverview[0],ProfitHistoryOverviewAndVolumeHistoryOverview[1],completedTokenList]
                }
                jsonWebsocketHistoryResponse = json.dumps(websocketHistoryResponse) 
                self.send(text_data=  jsonWebsocketHistoryResponse)

    return completedTokenList

def completeDetailedTokens(tokenArray,marketPrice,holdingsAmount,ethUSD,self):
    # GET THE TOKEN ADDRESS
    tokenContractAddress = tokenArray[2]
    print("--------------------------------------")
    print("TOKEN ARRAY BEFORE: ", tokenArray)
    print("HOLDINS AMOUNT: ", holdingsAmount)
    print("ETH TO USD: ", ethUSD)
    print("MARKET PRICE: ", marketPrice)
    if(holdingsAmount != -1):
        tokenArray[4] = holdingsAmount
    img_url = getTokenImage(tokenArray[0])
    if(tokenArray[4] <= 0):
        tokenArray[6] = 0
        tokenArray[7] = 0
    else:
        tokenArray[6] = tokenArray[4] * marketPrice * ethUSD
        tokenArray[7] = tokenArray[4] * marketPrice
        if(tokenContractAddress == "0x243cACb4D5fF6814AD668C3e225246efA886AD5a"):
            tokenArray[6] = tokenArray[4] * (122.188068/110000000000) * ethUSD
            tokenArray[7] = tokenArray[4] * (122.188068/110000000000)
        elif(tokenContractAddress == "0xbb9FD9Fa4863C03c574007fF3370787B9cE65ff6"):
            tokenArray[6] = tokenArray[4] * (10.990033/1064908.65207743142) * ethUSD
            tokenArray[7] = tokenArray[4] * (10.990033/1064908.65207743142)
        elif(tokenContractAddress == "0x8A2D988Fe2E8c6716cbCeF1B33Df626C692F7B98"):
            tokenArray[6] = tokenArray[4] * 0 * ethUSD
            tokenArray[7] = tokenArray[4] * 0
        elif(tokenContractAddress == "0x0ab87046fBb341D058F17CBC4c1133F25a20a52f"):
            tokenArray[6] = tokenArray[4] * 2.09 * ethUSD
            tokenArray[7] = tokenArray[4] * 2.09
        elif(tokenContractAddress == "0xf34960d9d60be18cC1D5Afc1A6F012A723a28811"):
            tokenArray[6] = tokenArray[4] * 0.0060 * ethUSD
            tokenArray[7] = tokenArray[4] * 0.0060
    tokenArray[9] = img_url
    print("TOKEN ARRAY AFTER: ", tokenArray)
    print("--------------------------------------")
    return tokenArray

def getTokenImage(tokenName):
    img_url = ""
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

def getTransfersPerToken(tokenList, normalTransaction, internalTransactions,checksumWalletAddress,ethUSD):
    tokenTransfers = dict()
    for tokens in tokenList:
        tokenAmountIn = 0
        tokenAmountOut = 0
        # Get Token Name
        tokenName = tokens.get('tokenName')
        # Get Token Symbol
        tokenSymbol = tokens.get('tokenSymbol')
        # Get Token Transaction Hash
        txHash = tokens.get("hash")
        # Get The From Address
        fromAddress = tokens.get('from')
        # WE ARE SENDING TOKENS OUT
        if(fromAddress == checksumWalletAddress.lower()):
            if(internalTransactions.get(txHash)):
                tokenAmountOut = internalTransactions.get(txHash) * ethUSD
        else:
            if(normalTransaction.get(txHash)):
                tokenAmountIn = normalTransaction.get(txHash) * ethUSD
        if(tokenTransfers.get(tokenName)):
            tokenTransfers.update({
                tokenName: [
                    tokenTransfers.get(tokenName)[0] + tokenAmountIn,
                    tokenTransfers.get(tokenName)[1] + tokenAmountOut
                ]
            })
        else:
            tokenTransfers.update({
                tokenName: [
                    tokenAmountIn,
                    tokenAmountOut
                ]
            })
    return tokenTransfers
    

def run(self, data):
    global GLOBAL_WALLET_ADDRESS
    global completedTokenList
    global priceAndAsset
    priceAndAsset.clear()
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    start_time = time.time()
    # GET WALLET ADDRESS
    walletAddress = data['walletAddress']

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

    # GET TRANSFERS PER TOKEN
    maxTokenTransfers =  getTransfersPerToken(maxERC20Transactions, maxDictNormalTransactions, maxDictInternalTransactions,checksumWalletAddress,ethUSD)
    yearlyTokenTransfers =  getTransfersPerToken(maxERC20Transactions, maxDictNormalTransactions, maxDictInternalTransactions,checksumWalletAddress,ethUSD)
    monthlyTokenTransfers =  getTransfersPerToken(maxERC20Transactions, maxDictNormalTransactions, maxDictInternalTransactions,checksumWalletAddress,ethUSD)
    weeklyTokenTransfers =  getTransfersPerToken(maxERC20Transactions, maxDictNormalTransactions, maxDictInternalTransactions,checksumWalletAddress,ethUSD)
    dailyTokenTransfers =  getTransfersPerToken(maxERC20Transactions, maxDictNormalTransactions, maxDictInternalTransactions,checksumWalletAddress,ethUSD)

    # GET INCOMPLETE TOKEN LIST
    maxDetailedTokens = getTokenDetailsAndProfit(maxERC20Transactions,maxDictNormalTransactions,maxDictInternalTransactions,checksumWalletAddress,ethUSD,maxTokenTransfers)
    yearlyDetailedTokens = getTokenDetailsAndProfit(yearlyERC20Transactions,yearlyDictNormalTransactions,yearlyDictInternalTransactions,checksumWalletAddress,ethUSD,yearlyTokenTransfers)
    monthlyDetailedTokens = getTokenDetailsAndProfit(monthlyERC20Transactions,monthlyDictNormalTransactions,monthlyDictInternalTransactions,checksumWalletAddress,ethUSD,monthlyTokenTransfers)
    weeklyDetailedTokens = getTokenDetailsAndProfit(weeklyERC20Transactions,weeklyDictNormalTransactions,weeklyDictInternalTransactions,checksumWalletAddress,ethUSD,weeklyTokenTransfers)
    dailyDetailedTokens = getTokenDetailsAndProfit(dailyERC20Transactions,dailyDictNormalTransactions,dailyDictInternalTransactions,checksumWalletAddress,ethUSD,dailyTokenTransfers)

    # SORT PROFIT LIST
    sortedMaxDetailedTokens = sortTokenDetailsAndProfit(maxDetailedTokens)
    sortedYearlyDetailedTokens = sortTokenDetailsAndProfit(yearlyDetailedTokens)
    sortedMonthlyDetailedTokens = sortTokenDetailsAndProfit(monthlyDetailedTokens)
    sortedWeeklyDetailedTokens = sortTokenDetailsAndProfit(weeklyDetailedTokens)
    sortedDailyDetailedTokens = sortTokenDetailsAndProfit(dailyDetailedTokens)
    # GET PROFIT HISTORY OVERVIEW
    maxProfitHistoryOverview = getProfitHistoryOverview(sortedMaxDetailedTokens,maxNormalTransactions,checksumWalletAddress,ethUSD)
    yearlyProfitHistoryOverview = getProfitHistoryOverview(sortedYearlyDetailedTokens,yearlyNormalTransactions,checksumWalletAddress,ethUSD)
    monthlyProfitHistoryOverview = getProfitHistoryOverview(sortedMonthlyDetailedTokens,monthlyNormalTransactions,checksumWalletAddress,ethUSD)
    weeklyProfitHistoryOverview = getProfitHistoryOverview(sortedWeeklyDetailedTokens,weeklyNormalTransactions,checksumWalletAddress,ethUSD)
    dailyProfitHistoryOverview = getProfitHistoryOverview(sortedDailyDetailedTokens,dailyNormalTransactions,checksumWalletAddress,ethUSD)
    
    # GET VOLUME HISTORY OVERVIEW
    maxVolumeHistoryOverview = getVolumeHistoryOverview(sortedMaxDetailedTokens,maxNormalTransactions,checksumWalletAddress,ethUSD)
    yearlyVolumeHistoryOverview = getVolumeHistoryOverview(sortedYearlyDetailedTokens,yearlyNormalTransactions,checksumWalletAddress,ethUSD)
    monthlyVolumeHistoryOverview = getVolumeHistoryOverview(sortedMonthlyDetailedTokens,monthlyNormalTransactions,checksumWalletAddress,ethUSD)
    weeklyVolumeHistoryOverview = getVolumeHistoryOverview(sortedWeeklyDetailedTokens,weeklyNormalTransactions,checksumWalletAddress,ethUSD)
    dailyVolumeHistoryOverview = getVolumeHistoryOverview(sortedDailyDetailedTokens,dailyNormalTransactions,checksumWalletAddress,ethUSD)
    
    ProfitHistoryOverviewAndVolumeHistoryOverview = [
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
    ]

    if(GLOBAL_WALLET_ADDRESS == walletAddress):
        websocketHistoryResponse = {
            'response' : [ProfitHistoryOverviewAndVolumeHistoryOverview[0],ProfitHistoryOverviewAndVolumeHistoryOverview[1],completedTokenList]
        }
        jsonWebsocketHistoryResponse = json.dumps(websocketHistoryResponse) 
        self.send(text_data=  jsonWebsocketHistoryResponse)
        return
    else:
        completedTokenList[0].clear()
        completedTokenList[1].clear()
        completedTokenList[2].clear()
        completedTokenList[3].clear()
        completedTokenList[4].clear()
    GLOBAL_WALLET_ADDRESS  = walletAddress
    # GET TOKEN ALLOTMENT AND MARKET PRICE IN ETH
    print("************** YEARLY **************")
    TokenAllotmentAndMarketPrice(sortedYearlyDetailedTokens,checksumWalletAddress,ethUSD,self,ProfitHistoryOverviewAndVolumeHistoryOverview,"yearly")
    print("************** YEARLY **************")
    TokenAllotmentAndMarketPrice(sortedMaxDetailedTokens,checksumWalletAddress,ethUSD,self,ProfitHistoryOverviewAndVolumeHistoryOverview,"max")
    TokenAllotmentAndMarketPrice(sortedMonthlyDetailedTokens,checksumWalletAddress,ethUSD,self,ProfitHistoryOverviewAndVolumeHistoryOverview,"monthly")
    TokenAllotmentAndMarketPrice(sortedWeeklyDetailedTokens,checksumWalletAddress,ethUSD,self,ProfitHistoryOverviewAndVolumeHistoryOverview,"weekly")
    TokenAllotmentAndMarketPrice(sortedDailyDetailedTokens,checksumWalletAddress,ethUSD,self,ProfitHistoryOverviewAndVolumeHistoryOverview,"daily")
    print("--- %s seconds ---" % (time.time() - start_time))
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
