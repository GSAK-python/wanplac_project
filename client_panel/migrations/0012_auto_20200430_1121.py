# Generated by Django 3.0.5 on 2020-04-30 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_panel', '0011_privacypolicy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacypolicy',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
