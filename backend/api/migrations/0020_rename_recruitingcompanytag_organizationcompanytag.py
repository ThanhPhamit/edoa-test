# Generated by Django 3.2.18 on 2023-08-13 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_rename_organizationrecruitingcompany_organizationcompany'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecruitingCompanyTag',
            new_name='OrganizationCompanyTag',
        ),
    ]
