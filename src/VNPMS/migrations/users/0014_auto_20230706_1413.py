# Generated by Django 3.0 on 2023-07-06 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20230703_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': (('perm_pms', '專案管理系統權限'), ('perm_ams', '資產管理系統權限'), ('perm_misc_apply', '總務用品請領申請單權限'), ('perm_workhour', '產線報工'), ('perm_user_manage', '使用者管理')), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
