# Generated by Django 4.1.4 on 2022-12-21 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0008_rename_topperformerconnections_overviewconnections'),
    ]

    operations = [
        migrations.AddField(
            model_name='overviewconnections',
            name='timeFrameTable',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
