# Generated by Django 3.0.5 on 2020-04-23 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_panel', '0007_auto_20200420_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
            ],
        ),
    ]