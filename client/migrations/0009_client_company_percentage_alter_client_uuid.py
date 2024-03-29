# Generated by Django 5.0 on 2024-01-17 15:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_rename_slack_channel_client_slack_channel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='company_percentage',
            field=models.IntegerField(default=15),
        ),
        migrations.AlterField(
            model_name='client',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Client Login License'),
        ),
    ]
