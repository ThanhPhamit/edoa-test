# coding: utf-8
import factory
import factory.fuzzy
from api.models import (
    Organization,
    User,
    RecruitingCompany,
    JobCategory,
    OrganizationCompany,
    Tag,
    Jobseeker,
    Job,
    Proposal,
    ProposalTag,
    Record,
)

from dataclasses import dataclass, asdict


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("word")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("word")
    name = factory.fuzzy.FuzzyText(length=5)
    email = factory.Sequence(lambda n: "person{}@example.com".format(n))
    password = factory.Faker("word")
    organization_id = factory.SubFactory(OrganizationFactory)


class RecruitingCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecruitingCompany

    corporate_number = factory.Sequence(lambda n: "0123456789{}".format(n))
    name = factory.fuzzy.FuzzyText(length=5)
    company_url = factory.Faker("url")
    recruiting_url = factory.Faker("url")
    logo = None
    establishment_date = factory.Faker("date")
    is_listed = factory.Faker("pybool")


class JobCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobCategory

    name = factory.Sequence(lambda n: "category{}".format(n))


class OrganizationCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganizationCompany

    summary = factory.Faker("sentence")
    total_employees = factory.Faker("random_number", digits=5)
    profit = factory.Faker("random_number", digits=5)
    service_years = factory.Faker("pyfloat")
    industry = factory.Faker("word")
    salary = factory.Faker("random_number", digits=5)
    age = factory.Faker("pyfloat")
    female_rate = factory.Faker("pyfloat")
    disabled_rate = factory.Faker("pyfloat")
    monthly_overtime_hours = factory.Faker("pyfloat")
    acquisition_rate = factory.Faker("pyfloat")
    childcare_leave_rate = factory.Faker("pyfloat")
    other = factory.Faker("sentence")
    recruiting_company_id = factory.SubFactory(RecruitingCompanyFactory)
    organization_id = factory.SubFactory(OrganizationFactory)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker("word")
    organization_id = factory.SubFactory(OrganizationFactory)


class JobseekerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Jobseeker

    name = factory.Faker("word")
    birth_date = factory.Faker("date")
    gender = factory.fuzzy.FuzzyText(length=5)
    phone_number = factory.Sequence(lambda n: "{}0123456789".format(n))
    in_charge_id = factory.SubFactory(UserFactory)
    last_record_at = factory.Faker("date_time")
    organization_id = factory.SubFactory(OrganizationFactory)


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    recruiting_company_id = factory.SubFactory(RecruitingCompanyFactory)
    organization_company_id = factory.SubFactory(OrganizationCompanyFactory)
    job_category_id = factory.SubFactory(JobCategoryFactory)
    position = factory.Faker("word")
    layer = factory.Faker("word")
    min_salary = factory.Faker("word")
    max_salary = factory.Faker("word")
    salary = factory.Faker("word")
    employment_status = factory.Faker("word")
    summary = factory.Faker("sentence")
    min_qualifications = factory.Faker("sentence")
    pfd_qualifications = factory.Faker("sentence")
    ideal_profile = factory.Faker("sentence")
    address = factory.Faker("sentence")
    remote = factory.Faker("word")
    working_hours = factory.Faker("sentence")
    holiday = factory.Faker("sentence")
    benefit = factory.Faker("sentence")
    trial_period = factory.Faker("word")
    smoking_prevention_measure = factory.Faker("word")
    other = factory.Faker("sentence")
    organization_id = factory.SubFactory(OrganizationFactory)


class ProposalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Proposal

    jobseeker_id = factory.SubFactory(JobseekerFactory)
    job_id = factory.SubFactory(JobFactory)
    intention = factory.fuzzy.FuzzyText(length=5)
    is_favorite = factory.Faker("pybool")
    comment = factory.Faker("sentence")
    is_public = factory.Faker("pybool")
    position = factory.Faker("word")
    salary = factory.Faker("word")
    summary = factory.Faker("sentence")
    min_qualifications = factory.Faker("sentence")
    pfd_qualifications = factory.Faker("sentence")
    ideal_profile = factory.Faker("sentence")
    is_appeal_layer = factory.Faker("pybool")
    is_appeal_remote = factory.Faker("pybool")
    organization_id = factory.SubFactory(OrganizationFactory)


class ProposalTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProposalTag

    proposal_id = factory.SubFactory(ProposalFactory)
    tag_id = factory.SubFactory(TagFactory)
    organization_id = factory.SubFactory(OrganizationFactory)


class RecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Record

    proposal_id = factory.SubFactory(ProposalFactory)
    before_record_at = factory.Faker("date_time")
    is_long_time = factory.Faker("pybool")
    is_checked = factory.Faker("pybool")
    trigger = factory.Faker("word")
    organization_id = factory.SubFactory(OrganizationFactory)
