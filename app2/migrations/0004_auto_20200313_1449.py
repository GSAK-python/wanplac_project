# Generated by Django 3.0.2 on 2020-03-13 13:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0003_datelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.CharField(default=datetime.date(2020, 3, 13), max_length=32),
        ),
    ]
