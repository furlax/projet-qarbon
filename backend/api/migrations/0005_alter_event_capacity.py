# Generated by Django 4.2 on 2023-05-25 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_event_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='capacity',
            field=models.IntegerField(default=2),
        ),
    ]
