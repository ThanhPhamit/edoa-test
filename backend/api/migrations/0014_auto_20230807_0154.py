# Generated by Django 3.2.18 on 2023-08-06 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_recruitingcompany_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationrecruitingcompany',
            name='age',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='organizationrecruitingcompany',
            name='service_years',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
