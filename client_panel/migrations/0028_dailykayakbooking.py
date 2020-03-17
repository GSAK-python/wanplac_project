# Generated by Django 3.0.2 on 2020-03-05 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_panel', '0027_dailykayak_protour'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyKayakBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_booking', to='client_panel.Booking')),
            ],
        ),
    ]