# Generated by Django 4.1.4 on 2022-12-21 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0009_overviewconnections_timeframetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overviewconnections',
            name='timeFrame',
            field=models.CharField(default='1H', max_length=30),
        ),
        migrations.AlterField(
            model_name='overviewconnections',
            name='timeFrameTable',
            field=models.CharField(default='1H', max_length=30),
        ),
    ]