# Generated by Django 3.0 on 2023-07-17 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20230714_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedform',
            name='apply_date',
            field=models.CharField(default='2023-07-17', max_length=10),
        ),
    ]