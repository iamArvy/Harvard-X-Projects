# Generated by Django 4.2.4 on 2023-12-08 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_message_read_by_alter_message_chat_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_sent_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='request_sent',
            field=models.BooleanField(default=False),
        ),
    ]