# Generated by Django 3.0 on 2023-01-03 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0021_doc_attachment_pic_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc_attachment',
            name='asset',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='asset_docs', to='assets.Asset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pic_attachment',
            name='asset',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='asset_pics', to='assets.Asset'),
            preserve_default=False,
        ),
    ]
