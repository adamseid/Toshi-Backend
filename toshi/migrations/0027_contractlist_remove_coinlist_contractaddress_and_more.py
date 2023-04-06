# Generated by Django 4.1.4 on 2023-01-30 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0026_remove_coinlist_identification_remove_coinlist_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='contractList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractAddress', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='coinlist',
            name='contractAddress',
        ),
        migrations.AddField(
            model_name='coinlist',
            name='identification',
            field=models.CharField(default=1, max_length=240, verbose_name='identification'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coinlist',
            name='name',
            field=models.CharField(default=1, max_length=240, verbose_name='name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coinlist',
            name='symbol',
            field=models.CharField(default=2, max_length=240, verbose_name='symbol'),
            preserve_default=False,
        ),
    ]