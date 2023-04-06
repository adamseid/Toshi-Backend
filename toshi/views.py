from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from .models import test
from .serializers import *
from .views_modules import History, Volume, AssetTable, PersonalPerformanceGraph, WalletBalance, Account, AccountHistory,HistoryV2

@api_view(['GET', 'POST'])
def history(request):
    if request.method == 'POST':
        frontEndData = request
        walletAddress = frontEndData.data['header']["walletAddress"]
        accountHistoryV2 = HistoryV2.run(walletAddress)
        # accountHistory = History.run(walletAddress)
        return(JsonResponse({"profile_response" : accountHistoryV2}))

@api_view(['GET', 'POST'])
def account(request):
    if request.method == 'POST':
        frontEndData = request
        walletAddress = frontEndData.data['header']["walletAddress"]
        accountOverview = Account.run(walletAddress)
        frontEndData.data['accountOverview']['table'] = [accountOverview]
        return(JsonResponse({"profile_response" : frontEndData.data}))

@api_view(['GET', 'POST'])
def volume_history_overview(request):
    if request.method == 'POST':
        frontEndData = request
        walletAddress = frontEndData.data['header']["walletAddress"]
        accountVolumeOverview = Volume.run(walletAddress)
        return(JsonResponse({"profile_response" : accountVolumeOverview}))

@api_view(['GET', 'POST'])
def accounthistory(request):
    if request.method == 'POST':
        frontEndData = request
        walletAddress = frontEndData.data['header']["walletAddress"]
        detailedAccounts = AccountHistory.run(walletAddress)
        return(JsonResponse({"profile_response" : detailedAccounts}))

@api_view(['GET', 'POST'])
def assetRequest(request):
    if request.method == 'POST':
        frontEndData = request
        walletAddress = request.data['header']["walletAddress"]
        # GET ASSETS
        assetTableData = AssetTable.run(walletAddress)
        frontEndData.data['profile']['table'] = list(assetTableData)
        return(JsonResponse({"profile_response" : frontEndData.data}))

@api_view(['GET', 'POST'])
def graphRequest(request):
    if request.method == 'POST':
        frontEndData = request
        walletAddress = request.data['header']["walletAddress"]
        # GET GRAPH DATA AND WALLET BALANCE
        graphData = PersonalPerformanceGraph.run(walletAddress)
        return(JsonResponse({"profile_response" : graphData}))

@api_view(['GET', 'POST'])
def accountGraphRequest(request):
    if request.method == 'POST':
        frontEndData = request
        walletAddress = request.data['header']["walletAddress"]
        # GET GRAPH DATA AND WALLET BALANCE
        graphData = PersonalPerformanceGraph.run(walletAddress)
        return(JsonResponse({"profile_response" : list(graphData)}))

@api_view(['GET', 'POST'])
def walletBalanceRequest(request):
    if request.method == 'POST':
        frontEndData = request
        walletAddress = request.data['header']["walletAddress"]
        ## GET Wallet Balance
        walletBalance = WalletBalance.run(walletAddress)
        return(JsonResponse({"profile_response" : walletBalance}))

@api_view(['GET', 'POST'])
def httpRequest(request):
    if request.method == 'POST':
        frontEndData = request
        walletAddress = request.data['header']["walletAddress"]
        ## GET ASSETS
        assetTableData = AssetTable.run(walletAddress)
        frontEndData.data['profile']['table'] = list(assetTableData)
        # GET GRAPH DATA AND WALLET BALANCE
        graphData = PersonalPerformanceGraph.run(walletAddress)
        frontEndData.data['profile']['graph'] = list(graphData)
        frontEndData.data['profile']['accountBalance'] = list(graphData)[3]
        return(JsonResponse({"profile_response" : frontEndData.data}))