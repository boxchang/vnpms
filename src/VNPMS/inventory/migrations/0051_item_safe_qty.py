# Generated by Django 3.2.23 on 2024-03-22 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0050_rename_stock_item_is_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='safe_qty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
