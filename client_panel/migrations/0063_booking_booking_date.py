# Generated by Django 3.0.2 on 2020-03-20 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_panel', '0062_bookingdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_date',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='client_panel.BookingDate'),
        ),
    ]