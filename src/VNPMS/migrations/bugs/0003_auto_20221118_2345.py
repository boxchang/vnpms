# Generated by Django 3.0 on 2022-11-18 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bases', '0002_auto_20221118_2345'),
        ('requests', '0001_initial'),
        ('projects', '0002_auto_20221118_2345'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bugs', '0002_bug_belong_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bug_create_at', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bug',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bus_level', to='requests.Level'),
        ),
        migrations.AddField(
            model_name='bug',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bugs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bug',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bug_project', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='bug',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bug_status', to='bases.Status'),
        ),
        migrations.AddField(
            model_name='bug',
            name='update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bug_update_at', to=settings.AUTH_USER_MODEL),
        ),
    ]
