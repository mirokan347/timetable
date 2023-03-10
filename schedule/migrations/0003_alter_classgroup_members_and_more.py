# Generated by Django 4.1.4 on 2023-02-05 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_parent_child_parent_students'),
        ('schedule', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classgroup',
            name='members',
            field=models.ManyToManyField(through='schedule.ClassGroupMembership', to='users.student'),
        ),
        migrations.AlterField(
            model_name='classgroupmembership',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
    ]
