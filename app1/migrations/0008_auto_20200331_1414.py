# Generated by Django 3.0.2 on 2020-03-31 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_auto_20200331_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='exact_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]