# Generated by Django 3.2.18 on 2023-08-06 15:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_job_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruitingcompany',
            name='close_date',
        ),
        migrations.RemoveField(
            model_name='recruitingcompany',
            name='import_date',
        ),
        migrations.AddField(
            model_name='recruitingcompany',
            name='establishment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recruitingcompany',
            name='is_listed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.organization')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitingCompanyTag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.organization')),
                ('recruiting_company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.recruitingcompany')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tag')),
            ],
        ),
        migrations.CreateModel(
            name='ProposalTag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.organization')),
                ('proposal_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.proposal')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tag')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationRecruitingCompany',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('summary', models.TextField(blank=True, max_length=1000)),
                ('total_employees', models.IntegerField(blank=True, null=True)),
                ('profit', models.BigIntegerField(blank=True, null=True)),
                ('service_years', models.SmallIntegerField(blank=True, null=True)),
                ('industry', models.CharField(max_length=50)),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('age', models.SmallIntegerField(blank=True, null=True)),
                ('female_rate', models.FloatField(blank=True, null=True)),
                ('disabled_rate', models.FloatField(blank=True, null=True)),
                ('monthly_overtime_hours', models.FloatField(blank=True, null=True)),
                ('acquisition_rate', models.FloatField(blank=True, null=True)),
                ('childcare_leave_rate', models.FloatField(blank=True, null=True)),
                ('other', models.TextField(blank=True, max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.organization')),
                ('recruiting_company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.recruitingcompany')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='recruiting_company_id',
            field=models.ManyToManyField(blank=True, through='api.OrganizationRecruitingCompany', to='api.RecruitingCompany'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='tag_id',
            field=models.ManyToManyField(blank=True, through='api.ProposalTag', to='api.Tag'),
        ),
        migrations.AddField(
            model_name='recruitingcompany',
            name='tag_id',
            field=models.ManyToManyField(blank=True, through='api.RecruitingCompanyTag', to='api.Tag'),
        ),
    ]