# Generated by Django 3.0 on 2023-07-14 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0016_auto_20230707_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='apply_date',
            field=models.CharField(default='2023-07-14', max_length=10),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='expect_date',
            field=models.CharField(default='2023-07-14', max_length=10),
        ),
    ]
