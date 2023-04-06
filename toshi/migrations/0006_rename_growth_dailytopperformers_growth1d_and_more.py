# Generated by Django 4.1.4 on 2022-12-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0005_personaltopperformancegraph_trendingtopperformers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dailytopperformers',
            old_name='growth',
            new_name='growth1D',
        ),
        migrations.RenameField(
            model_name='dailytopperformers',
            old_name='growthChange',
            new_name='growth1H',
        ),
        migrations.RenameField(
            model_name='trendingtopperformers',
            old_name='growth',
            new_name='growth1D',
        ),
        migrations.RenameField(
            model_name='trendingtopperformers',
            old_name='growthChange',
            new_name='growth1H',
        ),
        migrations.AddField(
            model_name='dailytopperformers',
            name='growth1M',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytopperformers',
            name='growth1W',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytopperformers',
            name='growth1Y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytopperformers',
            name='growthChange1D',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytopperformers',
            name='growthChange1H',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytopperformers',
            name='growthChange1M',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytopperformers',
            name='growthChange1W',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytopperformers',
            name='growthChange1Y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trendingtopperformers',
            name='growth1M',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trendingtopperformers',
            name='growth1W',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trendingtopperformers',
            name='growth1Y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trendingtopperformers',
            name='growthChange1D',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trendingtopperformers',
            name='growthChange1H',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trendingtopperformers',
            name='growthChange1M',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trendingtopperformers',
            name='growthChange1W',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trendingtopperformers',
            name='growthChange1Y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
