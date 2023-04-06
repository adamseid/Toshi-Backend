from django.contrib import admin
from .models import HistoryConnections, contracts,coinImages,AssetTable,coinList,ProfileConnections, TopPerformanceGraph, DailyTopPerformers, OverviewConnections, PersonalTopPerformanceGraph, TrendingTopPerformers, test, historic

# Register your models here.

admin.site.register(AssetTable)
admin.site.register(TopPerformanceGraph)
admin.site.register(DailyTopPerformers)
admin.site.register(OverviewConnections)
admin.site.register(PersonalTopPerformanceGraph)
admin.site.register(TrendingTopPerformers)
admin.site.register(ProfileConnections)
admin.site.register(test)
admin.site.register(historic)
admin.site.register(coinList)
admin.site.register(contracts)
admin.site.register(HistoryConnections)
admin.site.register(coinImages)