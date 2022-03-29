from statistics import mode
from tkinter import CASCADE

from django.contrib.auth.models import AbstractUser, User
from django.db import models

from models import Company


class JobCard(models.Model):
    id = models.AutoField(primary_key=True)
    job_card_number = models.CharField(max_length=100, null=True, blank=True)
    #job_card_client = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    job_card_client = models.CharField(max_length=100, null=True, blank=True)
    job_card_requester = models.CharField(max_length=100, null=True, blank=True)
    job_card_reference = models.CharField(max_length=100, null=True, blank=True)
    job_card_location = models.CharField(max_length=100, null=True, blank=True) # department
    job_card_created_at = models.DateTimeField(auto_now_add=True)
    job_card_started_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    Job_card_completed_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    #job_card_technician = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    job_card_technician = models.CharField(max_length=100, null=True, blank=True)
    job_card_type = models.CharField(max_length=100, null=True, blank=True)
    job_card_status = models.CharField(max_length=100, null=True, blank=True)
    job_card_description = models.TextField(null=True, blank=True)
    job_card_priority = models.CharField(max_length=100, null=True, blank=True, default='Normal')
    job_card_resolution = models.TextField(null=True, blank=True)
    job_card_completion_description = models.CharField(max_length=100, null=True, blank=True)
    job_card_nva_time = models.TimeField(null=True, blank=True)


# Create your models here.

#class CustomUsers(AbstractUser):
    #user_type_data = ((1, "sysAdmin"), (2, "Employee"), (3, "Comp_Admin"), (4, "Client"))
    #user_type = models.CharField(default=3, choices=user_type_data, max_length=10)   
    #company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    #USERNAME_FIELD = ['email']
    
'''
class Company(models.Model):
    companyId = models.AutoField(primary_key=True)
    companyName = models.CharField(max_length=100, default="Dummy Name")
    streetAddress = models.CharField(max_length=250)
    vatNum = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=50, unique=True, default="test@techkings.co.za")
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)

class Client(models.Model):
    clientId = models.AutoField(primary_key=True)
    clientName = models.CharField(max_length=100)
    streetAddress = models.CharField(max_length=250)
    vatNum = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=50, unique=True, default="")
'''
