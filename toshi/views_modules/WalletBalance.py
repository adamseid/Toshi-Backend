from ..views_modules import Misc
from requests import get
from requests import get
from datetime import datetime
from channels.layers import get_channel_layer
from Historic_Crypto import LiveCryptoData
from web3 import Web3

import time
import pandas as pd
from syncer import sync


FILE_NAME = 'Wallet Balance'
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
    walletBalance = generatewalletBalance(walletAddress)
    Misc.printDebug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

    return walletBalance


def generatewalletBalance(nonCheckSumWalletAddress):
    
    walletAddress = Web3.toChecksumAddress('0x' + str(nonCheckSumWalletAddress[-40:]))
    new =  LiveCryptoData('ETH-USD', verbose = False).return_data()
    account_balance = get_account_balance(walletAddress)*int(float(new['ask'][0]))
    return account_balance


def get_account_balance(wallet_address):
    balance_url = make_api_url(
        "account", "balance", wallet_address, tag="latest")
    response = get(balance_url)

    data = response.json()
    value = int(data["result"]) / ETHER_VALUE
    return value


def make_api_url(module, action, wallet_address, **kwargs):
    url = BASE_URL + \
        f"?module={module}&action={action}&address={wallet_address}&apikey={API_KEY}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url

