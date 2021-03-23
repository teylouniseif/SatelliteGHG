# Generated by Django 3.1.7 on 2021-03-21 00:45

from django.db import migrations, models
from django.contrib.postgres.operations import CreateExtension


class Migration(migrations.Migration):

    dependencies = [
        ('satellites', '0002_auto_20210320_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='elevation',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='target',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='target',
            name='long',
            field=models.FloatField(default=0),
        ),
        CreateExtension('postgis'),
    ]
