# Generated by Django 5.0 on 2023-12-26 07:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_contact_user_contact_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.useraddressbook'),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.payment'),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='shipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.shipment'),
        ),
    ]
