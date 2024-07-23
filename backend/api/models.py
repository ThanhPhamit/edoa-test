import uuid
import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"images/{uuid.uuid4()}.{ext}"
    return filename


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    companies = models.ManyToManyField(
        "Company",
        through="OrganizationCompany",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    password = models.CharField(max_length=128, blank=True, null=False)
    name = models.CharField(blank=True, null=False, max_length=50)
    organization = models.ForeignKey(
        "Organization", blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.organization} {self.name} {self.username}"


class Company(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    corporate_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150, db_index=True)
    company_url = models.CharField(blank=True, null=False, max_length=200)
    recruiting_url = models.CharField(blank=True, null=False, max_length=200)
    logo = models.ImageField(blank=True, null=True, upload_to=get_file_path)
    establishment_date = models.DateField(blank=True, null=True)
    is_listed = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        error = {}
        if len(self.corporate_number) != 13 or not re.fullmatch(
            r"^[0-9]{13}$", self.corporate_number
        ):
            error["corporate_number"] = "13桁の半角数字を入力してください"

        if re.search(r"[Ａ-Ｚａ-ｚ０-９]", self.name) or re.search(
            r"[ｦ-ﾟ｡-ﾟﾞｰ｢｣]", self.name
        ):
            error["name"] = "全角英数字または半角カナを入力できません"

        raise ValidationError(error)

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrganizationCompany(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "Company", blank=True, null=True, on_delete=models.CASCADE
    )
    name = models.CharField(blank=True, null=False, max_length=150, db_index=True)
    company_url = models.CharField(blank=True, null=False, max_length=200)
    summary = models.TextField(blank=True, null=False)
    total_employees = models.IntegerField(blank=True, null=True)
    profit = models.BigIntegerField(blank=True, null=True)
    service_years = models.FloatField(blank=True, null=True)
    industry = models.CharField(blank=True, null=False, max_length=50)
    salary = models.IntegerField(blank=True, null=True)
    age = models.FloatField(blank=True, null=True)
    female_rate = models.FloatField(blank=True, null=True)
    disabled_rate = models.FloatField(blank=True, null=True)
    monthly_overtime_hours = models.FloatField(blank=True, null=True)
    acquisition_rate = models.FloatField(blank=True, null=True)
    childcare_leave_rate = models.FloatField(blank=True, null=True)
    other = models.TextField(blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organization} {self.company}"


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Jobseeker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, db_index=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(blank=True, null=False, max_length=10)
    phone_number = models.CharField(
        blank=True, null=False, max_length=20, db_index=True
    )
    email = models.CharField(blank=True, null=False, max_length=100)
    in_charge = models.ForeignKey(
        "User", blank=True, null=True, on_delete=models.CASCADE
    )
    proposals = models.ManyToManyField(
        "Job",
        through="Proposal",
        blank=True,
    )
    last_record_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organization} {self.name}"


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_company = models.ForeignKey(
        "OrganizationCompany", blank=True, null=True, on_delete=models.CASCADE
    )
    job_category = models.ForeignKey(
        "JobCategory", on_delete=models.CASCADE, related_name="job"
    )
    position = models.TextField(blank=True, null=False)
    layer = models.CharField(blank=True, null=False, max_length=20)
    min_salary = models.IntegerField(blank=True, null=True)
    max_salary = models.IntegerField(blank=True, null=True)
    salary = models.TextField(blank=True, null=False)
    employment_status = models.CharField(blank=True, null=False, max_length=50)
    summary = models.TextField(blank=True, null=False)
    min_qualifications = models.TextField(blank=True, null=False)
    pfd_qualifications = models.TextField(blank=True, null=False)
    ideal_profile = models.TextField(blank=True, null=False)
    address = models.TextField(blank=True, null=False)
    remote = models.CharField(blank=True, null=False, max_length=20)
    working_hours = models.TextField(blank=True, null=False)
    holiday = models.TextField(blank=True, null=False)
    benefit = models.TextField(blank=True, null=False)
    trial_period = models.TextField(blank=True, null=False)
    smoking_prevention_measure = models.TextField(blank=True, null=False)
    other = models.TextField(blank=True, null=False)
    source_url = models.CharField(blank=True, null=False, max_length=500)
    is_archive = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organization} {self.organization_company} {self.position}"


class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jobseeker = models.ForeignKey("Jobseeker", on_delete=models.CASCADE)
    job = models.ForeignKey("Job", on_delete=models.CASCADE)
    position = models.TextField()
    salary = models.TextField(blank=True, null=False)
    employment_status = models.CharField(blank=True, null=False, max_length=50)
    summary = models.TextField(blank=True, null=False)
    min_qualifications = models.TextField(blank=True, null=False)
    pfd_qualifications = models.TextField(blank=True, null=False)
    ideal_profile = models.TextField(blank=True, null=False)
    address = models.TextField(blank=True, null=False)
    working_hours = models.TextField(blank=True, null=False)
    holiday = models.TextField(blank=True, null=False)
    benefit = models.TextField(blank=True, null=False)
    trial_period = models.TextField(blank=True, null=False)
    smoking_prevention_measure = models.TextField(blank=True, null=False)
    other = models.TextField(blank=True, null=False)
    intention = models.CharField(blank=True, null=False, max_length=10)
    comment = models.TextField(blank=True, null=False)
    tags = models.ManyToManyField(
        "Tag",
        through="ProposalTag",
        blank=True,
    )
    is_favorite = models.BooleanField(blank=True, null=True)
    is_public = models.BooleanField(blank=True, null=True, default=False)
    is_checked = models.BooleanField(default=True)
    is_appeal_layer = models.BooleanField(blank=True, null=True, default=False)
    is_appeal_remote = models.BooleanField(blank=True, null=True, default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.job} {self.jobseeker}"


class ProposalTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal = models.ForeignKey("Proposal", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)


class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal = models.ForeignKey("Proposal", on_delete=models.CASCADE)
    before_record_at = models.DateTimeField(blank=True, null=True)
    is_long_time = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    trigger = models.CharField(blank=True, null=False, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.proposal}"


class JobseekerHistoryNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.OneToOneField(Record, on_delete=models.CASCADE)
    is_send = models.BooleanField(blank=True, null=True, default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.record} {self.is_send}"


class JobLoading(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    source_url = models.CharField(max_length=500)
    is_completed = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=False)
    is_deleted = models.BooleanField(default=False)

    position = models.TextField(blank=True, null=False)
    salary = models.TextField(blank=True, null=False)
    employment_status = models.CharField(blank=True, null=False, max_length=50)
    summary = models.TextField(blank=True, null=False)
    min_qualifications = models.TextField(blank=True, null=False)
    pfd_qualifications = models.TextField(blank=True, null=False)
    ideal_profile = models.TextField(blank=True, null=False)
    address = models.TextField(blank=True, null=False)
    benefit = models.TextField(blank=True, null=False)
    other = models.TextField(blank=True, null=False)
    company_name = models.TextField(blank=True, null=False)
    job_category_name = models.CharField(blank=True, null=False, max_length=50)
    holiday = models.TextField(blank=True, null=False)
    working_hours = models.TextField(blank=True, null=False)
    smoking_prevention_measure = models.TextField(blank=True, null=False)
    trial_period = models.TextField(blank=True, null=False)
    layer = models.CharField(blank=True, null=False, max_length=20)
    remote = models.CharField(blank=True, null=False, max_length=20)
    min_salary = models.IntegerField(blank=True, null=True)
    max_salary = models.IntegerField(blank=True, null=True)

    telemetry_fetch_method = models.CharField(blank=True, null=False, max_length=50)
    telemetry_scraping_time = models.IntegerField(blank=True, null=True)
    telemetry_html_processing_names = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    telemetry_html_processing_results = ArrayField(models.IntegerField(), blank=True, null=True)
    telemetry_gpt_time = models.IntegerField(blank=True, null=True)
    telemetry_gpt_tokens_prompt = models.IntegerField(blank=True, null=True)
    telemetry_gpt_tokens_completion = models.IntegerField(blank=True, null=True)
    telemetry_error_detail = models.TextField(blank=True, null=False)
    telemetry_total_time = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if (self.is_error):
            return f"{self.user_id} {self.source_url[:20]} {self.error_message[:20]}"
        else:
            return f"{self.user_id} {self.source_url[:20]} {self.company_name} {self.position}"
