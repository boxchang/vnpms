# Generated by Django 3.0 on 2023-07-17 00:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('production', '0002_womain_enable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wo_no', models.CharField(blank=True, max_length=20, null=True)),
                ('emp_no', models.CharField(max_length=30)),
                ('sap_emp_no', models.CharField(blank=True, max_length=30, null=True)),
                ('cfm_code', models.CharField(blank=True, max_length=20, null=True)),
                ('step_code', models.CharField(blank=True, max_length=20, null=True)),
                ('step_name', models.CharField(blank=True, max_length=20, null=True)),
                ('record_dt', models.CharField(max_length=10)),
                ('labor_time', models.IntegerField(default=0)),
                ('mach_time', models.IntegerField(default=0)),
                ('good_qty', models.IntegerField(default=0)),
                ('ng_qty', models.IntegerField(default=0)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='record_create_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]