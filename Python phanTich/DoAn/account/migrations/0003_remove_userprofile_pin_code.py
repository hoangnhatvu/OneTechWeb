# Generated by Django 4.0.4 on 2022-05-17 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='pin_code',
        ),
    ]
