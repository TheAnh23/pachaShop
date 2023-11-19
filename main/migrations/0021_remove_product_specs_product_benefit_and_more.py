# Generated by Django 4.2.6 on 2023-11-19 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_banner_id_alter_brand_id_alter_cartorder_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='specs',
        ),
        migrations.AddField(
            model_name='product',
            name='benefit',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='ingredient',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='using',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=models.TextField(default=''),
        ),
    ]