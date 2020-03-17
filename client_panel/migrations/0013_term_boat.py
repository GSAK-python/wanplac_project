# Generated by Django 3.0.2 on 2020-03-03 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_panel', '0012_remove_booking_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='boat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='client_panel.Kayak'),
            preserve_default=False,
        ),
    ]