from ..top_performers_graph import Misc
from requests import get
from ...models import TopPerformanceGraph
from requests import get
from ...models import TopPerformanceGraph, DailyTopPerformers
from datetime import datetime
import time


FILE_NAME = 'TopPerformersGraph'
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

def update(wallet_address):
    wallet_address = wallet_address
    blockNumber = get_block_number(wallet_address)
    get_transactions(wallet_address,blockNumber)


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
        time = str(tx['timeStamp'])
        money_in = to.lower() == wallet_address.lower()
        if money_in:
            current_balance += value
        else:
            current_balance -= value + gas
        tpwp = TopPerformanceGraph(time=time, balance=current_balance)
        tpwp.save()
