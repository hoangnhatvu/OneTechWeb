# Generated by Django 4.0.4 on 2022-05-27 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variations',
        ),
    ]