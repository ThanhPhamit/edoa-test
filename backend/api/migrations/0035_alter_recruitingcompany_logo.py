# Generated by Django 3.2.18 on 2023-09-06 06:28

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20230904_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitingcompany',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.get_file_path),
        ),
    ]
