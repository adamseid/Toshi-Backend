
from celery import shared_task
from .task_modules import TopPerformersTable, TopPerformersGraph, TrendingWallets, Frontend, FrontendProfile


@shared_task(name='updateTopPerformersTable')
def updateTopPerformersTable():
    TopPerformersTable.update()


@shared_task(name='updateTopPerformersGraph')
def updateTopPerformersTableGraph():
    TopPerformersGraph.update()


@shared_task(name='updateTrendingWallets')
def updateTrendingWallets():
    TrendingWallets.update()


@shared_task(name='updateFrontend')
def updateFrontend():
    Frontend.update()

@shared_task(name='updateFrontendProfile')
def updateFrontendProfile():
    FrontendProfile.update()