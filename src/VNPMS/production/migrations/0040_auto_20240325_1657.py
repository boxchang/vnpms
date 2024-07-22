# Generated by Django 3.2.23 on 2024-03-25 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0039_delete_sync_sap_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumption',
            name='plant',
            field=models.CharField(default=True, max_length=10),
            preserve_default='',
        ),
        migrations.AddField(
            model_name='consumption',
            name='sap_flag',
            field=models.BooleanField(default=False),
        ),
    ]
