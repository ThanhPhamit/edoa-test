# Generated by Django 3.2.18 on 2023-09-12 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20230911_0321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='company',
        ),
        migrations.RemoveField(
            model_name='user',
            name='logo',
        ),
    ]
