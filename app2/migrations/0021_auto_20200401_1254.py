# Generated by Django 3.0.2 on 2020-04-01 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0019_auto_20200401_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='time',
            field=models.CharField(choices=[('', 'Kliknij'), ('9:00', '9:00'), ('9:30', '9:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00')], default='', max_length=32),
        ),
    ]
