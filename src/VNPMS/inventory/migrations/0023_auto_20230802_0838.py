# Generated by Django 3.0 on 2023-08-02 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_auto_20230801_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedform',
            name='apply_date',
            field=models.CharField(default='2023-08-02', max_length=10),
        ),
    ]
