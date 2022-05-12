from django.contrib import admin
from .models import JobCard, JobCardCategory, User, Address, Company, MaterialUsed, ClientUser

# Register your models here.
admin.site.register(JobCard)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Company)
admin.site.register(MaterialUsed)
admin.site.register(JobCardCategory)
admin.site.register(ClientUser)
