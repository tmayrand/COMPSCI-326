# Generated by Django 2.0.2 on 2018-03-20 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cloq', '0002_announcements_times'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='announcements',
            new_name='announcement',
        ),
        migrations.RenameModel(
            old_name='times',
            new_name='time',
        ),
    ]