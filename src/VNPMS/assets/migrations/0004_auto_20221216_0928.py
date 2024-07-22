# Generated by Django 3.0 on 2022-12-16 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_assetcategory_assettype_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='type_no',
        ),
        migrations.AddField(
            model_name='brand',
            name='category_no',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='category_brand', to='assets.AssetCategory'),
            preserve_default=False,
        ),
    ]
