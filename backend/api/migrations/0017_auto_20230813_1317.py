# Generated by Django 3.2.18 on 2023-08-13 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20230812_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='layer',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='job',
            name='remote',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]