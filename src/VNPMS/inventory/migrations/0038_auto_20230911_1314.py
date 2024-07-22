# Generated by Django 3.0 on 2023-09-11 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_auto_20230905_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliedform',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='form_category', to='inventory.ItemCategory'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appliedform',
            name='apply_date',
            field=models.CharField(default='2023-09-11', max_length=10),
        ),
    ]
