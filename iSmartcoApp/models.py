from secrets import choice
from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



class MaterialUsed(models.Model):
    material_name = models.CharField(max_length=100, null=True, blank=True)
    material_barcode = models.CharField(max_length=100, null=True, blank=True)	
    material_quantity = models.IntegerField(null=True, blank=True)
    material_unit = models.CharField(max_length=100, null=True, blank=True)
    material_price = models.IntegerField(null=True, blank=True)
    material_remarks = models.CharField(max_length=100, null=True, blank=True)
    material_job = models.ForeignKey('JobCard', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.material_name

class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    user_type_data = (("sysAdmin", "1"), ("CompAdmin", "2"), ("Client", "3"), ("Employee", "4"))
    user_type = models.CharField(max_length=10, choices=user_type_data, default="CompAdmin")
    user_company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    # user_address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True)
    # if user is CompAdmin then company is the company he belongs to
    # if user is Client then company is the company he is serviced by
    # if user is Employee then company is the company he works for
    # if user is sysAdmin then company is null

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # objects = MyAccountManager()

    def __str__(self):
        return self.email


'''
	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
	    return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)  
    def has_module_perms(self, app_label):
		return True
'''


class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True, default='South Africa')
    belongs_to = models.ManyToManyField(User, blank=True)
    is_active = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now=True)


class Client(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class JobCardCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    owned_by = models.ManyToManyField('Company', blank=True)
    def __str__(self):
        return self.name


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.EmailField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.name


class Employee(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id_num = models.CharField(max_length=13, unique=True)
    employee_name = models.CharField(max_length=50, null=True, blank=True)
    employee_phone = models.CharField(max_length=10, null=True, blank=True)
    employee_address = models.CharField(max_length=100, null=True, blank=True)
    employee_designation = models.CharField(max_length=50, null=True, blank=True)
    employee_joining_date = models.DateField(blank=True, null=True)
    employee_leaving_date = models.DateField(blank=True, null=True)
    employee_company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)


    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.employee_name


class JobCard(models.Model):
    id = models.AutoField(primary_key=True)
    job_card_number = models.IntegerField(null=False, default=0)  # unique for every company
    job_card_client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    job_card_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    # job_card_client = models.CharField(max_length=100, null=True, blank=True)
    job_card_reference = models.CharField(max_length=100, null=True,blank=True)  # can include invoice number or PO number
    #job_card_location = models.CharField(max_length=100, null=True, blank=True)  # department
    job_card_created_at = models.DateTimeField(auto_now_add=True)
    job_card_started_at = models.DateTimeField(auto_now_add=False, null=True, blank=True) #on PUT method
    job_card_completed_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    job_card_technicians = models.ManyToManyField(Employee, blank=True)
    job_card_status = models.CharField(max_length=100, null=True, blank=True)
    job_card_description = models.TextField(null=True, blank=True)
    priority_type_data = ((1, 'Low'), (2, 'Normal'), (3, 'High'))
    job_card_priority = models.CharField(max_length=100, choices=priority_type_data, default=3)
    job_card_resolution = models.TextField(null=True, blank=True)
    job_card_completion_description = models.CharField(max_length=100, null=True, blank=True)
    job_card_nva_time = models.TimeField(null=True, blank=True)  # describes the time in which nothing was done. Will be done in the frontend
    job_card_requester = models.ForeignKey('ClientUser', on_delete=models.CASCADE, null=True, blank=True)
    job_category = models.ForeignKey(JobCardCategory, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.job_card_number

class ClientUser(models.Model): #different users in each organization
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
