# Generated by Django 3.2.23 on 2024-01-09 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0040_auto_20230913_0828'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pic_attachment',
            old_name='asset',
            new_name='item',
        ),
    ]