# Generated by Django 4.2 on 2023-06-05 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_messagesusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagesusers',
            name='receiver_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='messagesusers',
            name='sender_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
