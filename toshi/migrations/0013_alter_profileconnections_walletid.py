# Generated by Django 4.1.4 on 2022-12-23 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0012_profileconnections'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileconnections',
            name='walletID',
            field=models.CharField(default='awaitingConnections', max_length=30),
        ),
    ]
