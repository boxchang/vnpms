# Generated by Django 3.2.23 on 2024-03-05 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0035_auto_20240305_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='record2',
            name='qty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
