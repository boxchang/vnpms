# Generated by Django 3.0 on 2023-08-01 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_auto_20230725_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedform',
            name='apply_date',
            field=models.CharField(default='2023-08-01', max_length=10),
        ),
    ]