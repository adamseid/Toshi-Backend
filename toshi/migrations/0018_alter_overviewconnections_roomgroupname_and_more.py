# Generated by Django 4.1.4 on 2022-12-23 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0017_alter_profileconnections_walletid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overviewconnections',
            name='roomGroupName',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='profileconnections',
            name='roomGroupName',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
