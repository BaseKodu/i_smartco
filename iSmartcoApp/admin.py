from django.contrib import admin
from .models import JobCard, Employee, User, Address, Company, Client

# Register your models here.
admin.site.register(JobCard)
admin.site.register(Employee)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Company)
admin.site.register(Client)
