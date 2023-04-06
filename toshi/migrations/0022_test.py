# Generated by Django 4.1.4 on 2023-01-08 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshi', '0021_alter_profileconnections_walletid'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
                ('email', models.EmailField(max_length=254)),
                ('document', models.CharField(max_length=20, verbose_name='Document')),
                ('phone', models.CharField(max_length=20)),
                ('registrationDate', models.DateField(auto_now_add=True, verbose_name='Registration Date')),
            ],
        ),
    ]


