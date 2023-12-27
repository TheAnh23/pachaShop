# Generated by Django 5.0 on 2023-12-23 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_product_brand_product_collection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='collection',
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.ManyToManyField(to='main.collection'),
        ),
    ]
