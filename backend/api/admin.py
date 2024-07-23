from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Organization
from .models import Company
from .models import JobCategory
from .models import OrganizationCompany
from .models import Tag
from .models import Jobseeker
from .models import Job
from .models import Proposal
from .models import ProposalTag
from .models import Record
from .models import JobseekerHistoryNotification
from .models import JobLoading


admin.site.register(Organization)
admin.site.register(get_user_model())
admin.site.register(Company)
admin.site.register(JobCategory)
admin.site.register(OrganizationCompany)
admin.site.register(Tag)
admin.site.register(Jobseeker)
admin.site.register(Job)
admin.site.register(Proposal)
admin.site.register(ProposalTag)
admin.site.register(Record)
admin.site.register(JobseekerHistoryNotification)
admin.site.register(JobLoading)
