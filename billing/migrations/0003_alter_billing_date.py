# Generated by Django 4.1.6 on 2023-02-26 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_alter_billing_typ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='date',
            field=models.DateField(),
        ),
    ]
