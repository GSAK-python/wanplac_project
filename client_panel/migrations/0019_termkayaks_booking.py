# Generated by Django 3.0.2 on 2020-03-04 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_panel', '0018_auto_20200304_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='termkayaks',
            name='booking',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bookingss', to='client_panel.Booking'),
            preserve_default=False,
        ),
    ]
