# Generated by Django 4.2.4 on 2023-11-13 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_user_auctions'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='desc',
            field=models.TextField(blank=True, max_length=120, null=True),
        ),
    ]
