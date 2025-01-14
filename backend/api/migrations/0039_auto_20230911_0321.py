# Generated by Django 3.2.18 on 2023-09-10 18:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0038_proposal_published_at"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="RecruitingCompany",
            new_name="Company",
        ),
        migrations.RenameField(
            model_name="job",
            old_name="recruiting_company_id",
            new_name="company",
        ),
        migrations.RenameField(
            model_name="job",
            old_name="job_category_id",
            new_name="job_category",
        ),
        migrations.RenameField(
            model_name="job",
            old_name="organization_id",
            new_name="organization",
        ),
        migrations.RenameField(
            model_name="job",
            old_name="organization_company_id",
            new_name="organization_company",
        ),
        migrations.RenameField(
            model_name="jobseeker",
            old_name="in_charge_id",
            new_name="in_charge",
        ),
        migrations.RenameField(
            model_name="jobseeker",
            old_name="organization_id",
            new_name="organization",
        ),
        migrations.RenameField(
            model_name="jobseekerhistorynotification",
            old_name="organization_id",
            new_name="organization",
        ),
        migrations.RenameField(
            model_name="organizationcompany",
            old_name="recruiting_company_id",
            new_name="company",
        ),
        migrations.RenameField(
            model_name="organizationcompany",
            old_name="organization_id",
            new_name="organization",
        ),
        migrations.RenameField(
            model_name="proposal",
            old_name="job_id",
            new_name="job",
        ),
        migrations.RenameField(
            model_name="proposal",
            old_name="jobseeker_id",
            new_name="jobseeker",
        ),
        migrations.RenameField(
            model_name="proposal",
            old_name="organization_id",
            new_name="organization",
        ),
        migrations.RenameField(
            model_name="proposal",
            old_name="tag_id",
            new_name="tags",
        ),
        migrations.RenameField(
            model_name="proposaltag",
            old_name="organization_id",
            new_name="organization",
        ),
        migrations.RenameField(
            model_name="proposaltag",
            old_name="proposal_id",
            new_name="proposal",
        ),
        migrations.RenameField(
            model_name="proposaltag",
            old_name="tag_id",
            new_name="tag",
        ),
        migrations.RenameField(
            model_name="record",
            old_name="organization_id",
            new_name="organization",
        ),
        migrations.RenameField(
            model_name="record",
            old_name="proposal_id",
            new_name="proposal",
        ),
        migrations.RenameField(
            model_name="tag",
            old_name="organization_id",
            new_name="organization",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="organization_id",
            new_name="organization",
        ),
        migrations.RenameField(
            model_name="organization",
            old_name="recruiting_company_id",
            new_name="companies",
        ),
    ]
