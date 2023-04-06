from requests import get
from web3 import Web3
from ..views_modules import Misc
import json
import concurrent.futures

from ..models import coinList,coinImages

erc20TokenAbi = [{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"}]
uniswapAbi = [{"inputs": [],"name": "getReserves","outputs": [{"internalType": "uint112","name": "_reserve0","type": "uint112"},{"internalType": "uint112","name": "_reserve1","type": "uint112"},{"internalType": "uint32","name": "_blockTimestampLast","type": "uint32"}],"stateMutability": "view","type": "function"},{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]

web3eth = Web3(Web3.HTTPProvider("https://eth-mainnet.g.alchemy.com/v2/_mEa4ksrzCdb8fgB5_7-4doIZrMWwpKf"))
API_KEY = "239PUCE9PMQCURRRZPVXRBESYPF4HUHRMZ"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18
unix_hour = 3600
unix_day = 86400
unix_week = 604800
unix_month = 2628000
unix_year = 31540000

FILE_NAME = 'AssetTable'
DEBUG = True

def run(walletAddress):
    FUNCTION_NAME = 'run'
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    # print(web3eth.eth.get_transaction("0x580c207a9e210a41a0886ee3ed937a5e10ed18258967c8348a780cdca6b09e70"))
    checkSumwalletAddress = getCheckSumWalletAddress(walletAddress)
    erc20Transactions = getERC20Transactions(walletAddress=checkSumwalletAddress)
    assetData = getAssets(erc20Transactions)
    checkedAssetData = getAssetAmmount(assetData,checkSumwalletAddress)
    assetDataWithUSD,USDTotal = getAssetInUSD(checkedAssetData)
    completedAssetData = getAssetAllocationAndImage(assetDataWithUSD,USDTotal)
    sortedDetailedAssets = sortAssets(completedAssetData)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
    return sortedDetailedAssets

def getAssetAmmount(assets,walletAddress):
    refinedAssets = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(refineAssets, asset, walletAddress, assets) for asset in assets]
        for future in concurrent.futures.as_completed(futures):
            try:
                asset, assetArray = future.result()
                refinedAssets[asset] = assetArray
            except: 
                print("Error in GetAssetAmmount")
    return refinedAssets

def refineAssets(asset, walletAddress, assets):
    # Get an array of asset details of each asset
    assetArray = assets.get(asset)
    # Set the addresses of the token, exchange contracts, Eth, and USD
    tokenAddress = assetArray [5]
    # Get the contract instances for the token and exchange
    token = web3eth.eth.contract(address=tokenAddress, abi=json.loads(json.dumps(erc20TokenAbi))) # declaring the token contract
    # Get the token balance in wei
    rawBalance = token.functions.balanceOf(walletAddress).call()
    # Get the token decimal
    token_decimals = token.functions.decimals().call()      
    # Get balance in token amount
    balance = rawBalance / (10 ** token_decimals)
    # Replace old token amount with new token amount
    assetArray[2] = balance
    return asset, assetArray
    

def getAssetAllocationAndImage(assetData, totalUSD):
    detailedAssets = []
    for asset in assetData:
        assetArray = assetData.get(asset)
        assetArray[4] = round((assetArray[3]/totalUSD)*100,2)
        if(assetArray[0] == "Toshi Tools"):
            assetArray.append("https://etherscan.io/token/images/toshitools_32.png")
        elif(assetArray[0] == "Tether USD"):
            assetArray.append("https://assets.coingecko.com/coins/images/325/thumb/Tether.png?1668148663")
        elif(coinList.objects.filter(name=assetArray[0])):
            identity = coinList.objects.filter(name=assetArray[0]).values()[0]['identification']   
            if(coinImages.objects.filter(identification = identity)):
                image_url = coinImages.objects.filter(identification = identity).values()[0].get("image_url")
                assetArray.append(image_url)
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
                    assetArray.append(data.get("image").get("thumb"))
        detailedAssets.append(assetArray)
    return detailedAssets


def getAssetInUSD(assetData):
    totalUSD = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(assetInUSD, asset, assetData, totalUSD) for asset in assetData]
        for future in concurrent.futures.as_completed(futures):
            try:
                asset, assetArray, totalUSD = future.result()
                assetData[asset] = assetArray
            except:
                print("Error in getAssetInUSD")
    if(totalUSD == 0):
        totalUSD = 1
    return assetData,totalUSD

def assetInUSD(asset, assetData, totalUSD):
    print(asset)
    assetArray = assetData.get(asset)
    contractAddress = assetArray[5]
    tokenAmount = assetArray[2]
    marketPrice = getMarketPrice(contractAddress)
    tokenAmountUSD = marketPrice * tokenAmount
    if(tokenAmountUSD >= 0.001):
        assetArray[3] = round(tokenAmountUSD,2)
    else:
        assetArray[3] = tokenAmountUSD
        
    if(assetArray[2] >= 0.001):
        assetArray[2] = round(assetArray[2],2)

    totalUSD = totalUSD + tokenAmountUSD

    return asset, assetArray, totalUSD


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
    token_to_eth_price_wei = [0,0]
    try:
        token_to_eth_price_wei = exchange_contract.functions.getAmountsOut(token_input_amount, token_path).call()
    except Exception as e:
        print("TOKEN DOES NOT EXIST ON EXCHANGE")
    eth_to_usd_price_wei = exchange_contract.functions.getAmountsOut(exchange_input_amount, exchange_path).call()

    # Get the token exhange rates in the proper units
    token_to_eth_price_eth = token_to_eth_price_wei[1]/(10**exchange_decimal)
    eth_to_usd_price_usd = eth_to_usd_price_wei[1]/(10**usd_decimal)

    # Get current market price of token in USD
    token_market_price = token_to_eth_price_eth * eth_to_usd_price_usd
    return token_market_price

def sortAssets(assets):
    sorted_array = sorted(assets, key=lambda x: x[3],reverse=True)
    return sorted_array

def getAssets(erc20Transactions):
    tokenInfoAndAllocation = dict()
    # Iterate through all token transfer events
    for tokensTransfers in erc20Transactions:
        # Get Token Name
        tokenName = tokensTransfers['tokenName']
        # Get Token Symbol
        tokenSymbol = tokensTransfers['tokenSymbol']
        # Get Token Allocation
        contractAddress = getCheckSumWalletAddress(tokensTransfers.get("contractAddress"))
        # If the token is not within our list
        if(not tokenInfoAndAllocation.get(tokenName)):
            tokenInfoAndAllocation.update({
                    tokenName: [
                        tokenName, # Token Name
                        tokenSymbol, # Token Acronym
                        0, # Asset Allocation
                        0, # token Amount USD
                        0, # Asset Allocation Percentage
                        contractAddress
                    ]
                })
    return tokenInfoAndAllocation

def getCheckSumWalletAddress(nonCheckSumWalletAddress):
    return Web3.toChecksumAddress('0x' + str(nonCheckSumWalletAddress[-40:]))

def getERC20Transactions(walletAddress):
    transactions_url = make_api_url(
        "account", 
        "tokentx", 
        walletAddress,
        startblock=1, 
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
