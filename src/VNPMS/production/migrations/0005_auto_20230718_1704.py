# Generated by Django 3.0 on 2023-07-18 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0004_auto_20230717_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exceltemp',
            name='wo_labor_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='exceltemp',
            name='wo_mach_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='labor_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='mach_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='wodetail',
            name='wo_labor_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='wodetail',
            name='wo_mach_time',
            field=models.FloatField(default=0),
        ),
    ]