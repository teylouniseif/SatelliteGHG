# Generated by Django 3.1.7 on 2021-03-21 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('satellites', '0006_auto_20210321_0610'),
    ]

    operations = [
        migrations.RenameField(
            model_name='observation',
            old_name='uploaded_at',
            new_name='timestamp',
        ),
    ]
