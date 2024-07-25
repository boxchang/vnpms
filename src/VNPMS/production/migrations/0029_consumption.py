# Generated by Django 3.2.23 on 2024-02-20 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('production', '0028_record_mach'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wo_no', models.CharField(max_length=20)),
                ('item_no', models.CharField(max_length=20)),
                ('qty', models.FloatField(default=0)),
                ('create_at', models.DateTimeField(auto_now=True, null=True)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='consumption_create_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]