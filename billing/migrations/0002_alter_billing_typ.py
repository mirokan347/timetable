# Generated by Django 4.1.4 on 2023-02-08 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='typ',
            field=models.CharField(choices=[('Payment', 'Payment'), ('Bill', 'Bill')], max_length=10),
        ),
    ]
