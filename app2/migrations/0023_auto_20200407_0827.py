# Generated by Django 3.0.5 on 2020-04-07 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0021_auto_20200407_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='exact_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='termkayaks',
            name='exact_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
