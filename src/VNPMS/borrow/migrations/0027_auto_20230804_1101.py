# Generated by Django 3.0 on 2023-08-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0026_auto_20230802_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='apply_date',
            field=models.CharField(default='2023-08-04', max_length=10),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='expect_date',
            field=models.CharField(default='2023-08-04', max_length=10),
        ),
    ]