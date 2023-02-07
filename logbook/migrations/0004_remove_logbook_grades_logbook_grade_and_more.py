# Generated by Django 4.1.4 on 2023-02-05 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logbook', '0003_remove_comment_student_remove_comment_teacher_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logbook',
            name='grades',
        ),
        migrations.AddField(
            model_name='logbook',
            name='grade',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='logbook',
            name='attendance',
            field=models.CharField(blank=True, choices=[('P', 'Present'), ('A', 'Absent'), ('E', 'Excused')], default=None, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='logbook',
            name='comment',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
    ]