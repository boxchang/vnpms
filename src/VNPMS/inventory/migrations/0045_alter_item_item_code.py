# Generated by Django 3.2.23 on 2024-03-13 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0044_alter_itemcategory_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_code',
            field=models.CharField(max_length=11),
        ),
    ]