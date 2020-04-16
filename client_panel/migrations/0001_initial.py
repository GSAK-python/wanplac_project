# Generated by Django 3.0.5 on 2020-04-16 12:41

import client_panel.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=32)),
                ('last_name', models.CharField(blank=True, max_length=32)),
                ('time', models.CharField(choices=[('', 'Kliknij'), ('9:00', '9:00'), ('9:30', '9:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00')], default='', max_length=32)),
                ('phone', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('exact_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookingDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DateList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Kayak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('stock', models.IntegerField()),
                ('store', models.IntegerField()),
                ('type', models.CharField(choices=[('Jednosoboy', 'Jednoosobwy'), ('Dwuosobowy', 'Dwuosobowy'), ('Trzyosobowy', 'Trzyosobowy')], max_length=32)),
                ('available', models.BooleanField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('distance', models.CharField(max_length=32)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TermKayaks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('exact_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='term_bookings', to='client_panel.Booking')),
                ('kayak', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kayaks', to='client_panel.Kayak')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_date',
            field=models.ForeignKey(default='', limit_choices_to=client_panel.models.booking_dates_limit, on_delete=django.db.models.deletion.CASCADE, related_name='cp_booking_date', to='client_panel.BookingDate'),
        ),
        migrations.AddField(
            model_name='booking',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client_panel.Route'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunSQL("UPDATE SQLITE_SEQUENCE SET SEQ=1000 WHERE NAME='client_panel_bookingdate';")
    ]
