# Generated by Django 3.0.2 on 2020-03-05 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_panel', '0022_kayak_available_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='daily_kayaks',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='daily_kayaks', to='client_panel.Kayak'),
            preserve_default=False,
        ),
    ]