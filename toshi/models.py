from django.db import models

# Create your models here.

# PROFILE PAGE DATABASES


class AssetTable(models.Model):
    tokenName = models.CharField(max_length=30)
    tokenAbbreviation = models.CharField(max_length=30)
    AmountInEth = models.FloatField()
    tokenAllocation = models.FloatField()
    AmountInEthUSD = models.FloatField()
    changeInTokenPrice = models.FloatField()


class PersonalTopPerformanceGraph(models.Model):
    time = models.CharField(max_length=30, primary_key=True)
    balance = models.FloatField()

# OVERVIEW PAGE DATABASES


class TopPerformanceGraph(models.Model):
    time = models.CharField(max_length=30, primary_key=True)
    balance = models.FloatField()


class DailyTopPerformers(models.Model):
    walletAddress = models.CharField(max_length=50)
    Asset = models.CharField(max_length=30, primary_key=True)
    growth1H = models.FloatField()
    growth1D = models.FloatField()
    growth1W = models.FloatField()
    growth1M = models.FloatField()
    growth1Y = models.FloatField()
    growthChange1H = models.FloatField()
    growthChange1D = models.FloatField()
    growthChange1W = models.FloatField()
    growthChange1M = models.FloatField()
    growthChange1Y = models.FloatField()


class TrendingTopPerformers(models.Model):
    walletAddress = models.CharField(max_length=50)
    Asset = models.CharField(max_length=30, primary_key=True)
    growth1H = models.FloatField()
    growth1D = models.FloatField()
    growth1W = models.FloatField()
    growth1M = models.FloatField()
    growth1Y = models.FloatField()
    growthChange1H = models.FloatField()
    growthChange1D = models.FloatField()
    growthChange1W = models.FloatField()
    growthChange1M = models.FloatField()
    growthChange1Y = models.FloatField()


# REACT-DJANGO DATABASES

class OverviewConnections(models.Model):
    roomGroupName = models.CharField(max_length=30, unique=True)
    timeFrame = models.CharField(max_length=30, default='1H')
    timeFrameTable = models.CharField(max_length=30, default='1H')

class ProfileConnections (models.Model):
    roomGroupName = models.CharField(max_length=30)
    timeFrame = models.CharField(max_length=30, default='1M')
    walletID = models.CharField(max_length=50)

class HistoryConnections (models.Model):
    roomGroupName = models.CharField(max_length=30)
    walletID = models.CharField(max_length=50)

# TEST DATABASE
class test(models.Model):
    name = models.CharField("Name", max_length=240)
    email = models.EmailField()
    document = models.CharField("Document", max_length=20)
    phone = models.CharField(max_length=20)
    registrationDate = models.DateField("Registration Date", auto_now_add=True)

    def __str__(self):
        return self.name

# HISTORIC CRYPTO DATA
class historic(models.Model):
    token = models.CharField("token", max_length=240)
    date = models.CharField("date", max_length=240)
    price = models.FloatField()

# COIN GECKO CRYPTO DATA LIST
class coinList(models.Model):
    identification = models.CharField("identification", max_length=240)
    symbol = models.CharField("symbol", max_length=240)
    name = models.CharField("name", max_length=240)

# COIN GECKO CRYPTO Token Images
class coinImages(models.Model):
    identification = models.CharField("identification", max_length=240)
    image_url = models.CharField("image_url", max_length=240)

    def __str__(self):
        return self.identification

# contract Address list
class contracts(models.Model):
    contractAddress = models.CharField(max_length=50)
