# Generated by Django 4.1.6 on 2023-02-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_phone'),
        ('schedule', '0005_alter_lesson_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='students',
            field=models.ManyToManyField(blank=True, to='users.student'),
        ),
    ]
