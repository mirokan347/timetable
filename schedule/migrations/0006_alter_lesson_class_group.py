# Generated by Django 4.1.4 on 2023-01-23 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_lesson_pupil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='class_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.classgroup'),
        ),
    ]