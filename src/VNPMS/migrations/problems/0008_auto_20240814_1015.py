# Generated by Django 3.2.25 on 2024-08-14 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0007_auto_20240807_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='dept',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Problem Dept'),
        ),
        migrations.AddField(
            model_name='problem',
            name='plant',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Problem Plant'),
        ),
    ]