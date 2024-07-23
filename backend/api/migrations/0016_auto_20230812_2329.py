# Generated by Django 3.2.18 on 2023-08-12 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_organizationrecruitingcompany_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruitingcompany',
            name='tag_id',
        ),
        migrations.RemoveField(
            model_name='recruitingcompanytag',
            name='recruiting_company_id',
        ),
        migrations.AddField(
            model_name='organizationrecruitingcompany',
            name='tag_id',
            field=models.ManyToManyField(blank=True, through='api.RecruitingCompanyTag', to='api.Tag'),
        ),
        migrations.AddField(
            model_name='recruitingcompanytag',
            name='organization_recruiting_company_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.organizationrecruitingcompany'),
        ),
    ]