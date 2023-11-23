# Generated by Django 4.1.13 on 2023-11-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='image',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='images',
            field=models.ManyToManyField(to='main.image'),
        ),
    ]