# Generated by Django 4.0.4 on 2022-05-24 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_last_visit_product_num_visit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_order',
            field=models.IntegerField(default=0),
        ),
    ]