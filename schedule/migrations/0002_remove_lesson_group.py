# Generated by Django 4.1.4 on 2022-12-21 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='group',
        ),
    ]
