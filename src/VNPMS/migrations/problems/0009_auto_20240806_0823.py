# Generated by Django 3.2.25 on 2024-08-06 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0008_auto_20240805_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='publisher',
        ),
        migrations.AlterField(
            model_name='problem',
            name='issue_owner',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Owner'),
        ),
    ]
