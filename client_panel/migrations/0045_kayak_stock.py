# Generated by Django 3.0.2 on 2020-03-14 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_panel', '0044_auto_20200313_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='kayak',
            name='stock',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]