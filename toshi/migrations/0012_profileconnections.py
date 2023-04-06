# Generated by Django 4.1.4 on 2022-12-23 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0011_alter_dailytopperformers_walletaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileConnections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomGroupName', models.CharField(max_length=30)),
                ('timeFrame', models.CharField(default='1H', max_length=30)),
                ('walletID', models.CharField(default='notConnected', max_length=30)),
            ],
        ),
    ]