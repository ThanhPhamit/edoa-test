# Generated by Django 3.2.18 on 2023-08-25 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20230825_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='organization_company_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.organizationcompany'),
        ),
    ]
