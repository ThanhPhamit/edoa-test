# Generated by Django 3.2.18 on 2023-08-29 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_organizationcompany_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationcompany',
            name='company_url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]