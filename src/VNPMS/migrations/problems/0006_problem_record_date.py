# Generated by Django 3.2.25 on 2024-08-05 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_problem_problem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='record_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Record Date'),
        ),
    ]