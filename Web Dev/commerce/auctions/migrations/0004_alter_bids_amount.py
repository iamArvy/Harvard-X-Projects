# Generated by Django 4.2.4 on 2023-11-11 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_user_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
