# Generated by Django 4.1.4 on 2022-12-23 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0018_alter_overviewconnections_roomgroupname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileconnections',
            name='timeFrame',
            field=models.CharField(default='1M', max_length=30),
        ),
    ]