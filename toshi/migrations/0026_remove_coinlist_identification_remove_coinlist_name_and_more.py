# Generated by Django 4.1.4 on 2023-01-30 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0025_coinlist_alter_historic_date_alter_historic_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coinlist',
            name='identification',
        ),
        migrations.RemoveField(
            model_name='coinlist',
            name='name',
        ),
        migrations.RemoveField(
            model_name='coinlist',
            name='symbol',
        ),
        migrations.AddField(
            model_name='coinlist',
            name='contractAddress',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]