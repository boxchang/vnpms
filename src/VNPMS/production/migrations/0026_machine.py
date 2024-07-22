# Generated by Django 3.0 on 2023-11-07 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0025_auto_20230913_0824'),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_code', models.CharField(blank=True, max_length=20, null=True)),
                ('step_name', models.CharField(blank=True, max_length=20, null=True)),
                ('mach_code', models.CharField(blank=True, max_length=20, null=True)),
                ('mach_name', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
