# Generated by Django 5.0 on 2023-12-26 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_cartorder_address_cartorder_payment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddressbook',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
