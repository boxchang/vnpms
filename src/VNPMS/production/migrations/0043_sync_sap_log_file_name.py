# Generated by Django 3.2.23 on 2024-03-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0042_sync_sap_log_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='sync_sap_log',
            name='file_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
