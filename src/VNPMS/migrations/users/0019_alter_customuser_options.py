# Generated by Django 3.2.23 on 2024-03-07 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20230829_1030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': (('perm_pms', '專案管理系統權限'), ('perm_ams', '資產管理系統權限'), ('perm_misc_apply', '總務用品請領管理者權限'), ('perm_workhour', '產線報工'), ('perm_user_manage', '使用者管理'), ('perm_svr_monitor', '伺服器監控')), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]