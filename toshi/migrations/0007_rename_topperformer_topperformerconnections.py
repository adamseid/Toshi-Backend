# Generated by Django 4.1.4 on 2022-12-21 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0006_rename_growth_dailytopperformers_growth1d_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TopPerformer',
            new_name='TopPerformerConnections',
        ),
    ]
