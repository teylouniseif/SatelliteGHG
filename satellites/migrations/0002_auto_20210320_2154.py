# Generated by Django 3.1.7 on 2021-03-20 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellites', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='observation',
            old_name='Input',
            new_name='image',
        ),
    ]
