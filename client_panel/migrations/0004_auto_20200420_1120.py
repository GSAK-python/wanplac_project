# Generated by Django 3.0.5 on 2020-04-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_panel', '0003_auto_20200420_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kayak',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/media'),
        ),
    ]
