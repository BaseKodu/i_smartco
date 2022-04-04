from django.contrib import admin
from .models import JobCard, JobCardCategory, Employee, User, Address, Company, Client, MaterialUsed

# Register your models here.
admin.site.register(JobCard)
admin.site.register(Employee)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Company)
admin.site.register(Client)
admin.site.register(MaterialUsed)
admin.site.register(JobCardCategory)
