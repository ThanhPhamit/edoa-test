# Generated by Django 3.2.18 on 2023-08-07 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20230807_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationrecruitingcompany',
            name='industry',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]