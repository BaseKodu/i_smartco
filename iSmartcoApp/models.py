from statistics import mode
from tkinter import CASCADE

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pytz import timezone


'''
class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)gg

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user
'''


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    user_type_data = ((1,"sysAdmin"),(2,"CompanyAdmin"), (3,"Client"), (4,"Employee"))
    user_type = models.IntegerField(choices=user_type_data, default=2)
    user_company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    #if user is CompAdmin then company is the company he belongs to
    #if user is Client then company is the company he is serviced by
    #if user is Employee then company is the company he works for
    #if user is sysAdmin then company is null
    #user_address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True) # a user can have a lot of addresses
    #phone = models.CharField(max_length=100, null=True, blank=True) # foreign key. User will have mamy phone numbers
    user_id_num = models.CharField(max_length=50, unique=False, null = True, blank=True) # for org clients, it will be business reg number
    designation = models.CharField(max_length=100, null=True, blank=True) # designation is for employees on what role they work on
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    #objects = MyAccountManager()

    def __str__(self):
    	return self.email



class Phone(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100)
    dialing_code = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number

'''	
class Client(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class Employee(models.Model):
    #before production, remember to accomodate for users in other countries
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id_num = models.CharField(max_length=13, unique=False)
    employee_name = models.CharField(max_length=50, null=True, blank=True)
    employee_phone = models.CharField(max_length=10, null=True, blank=True)
    employee_address = models.CharField(max_length=100, null=True, blank=True)
    employee_designation = models.CharField(max_length=50, null=True, blank=True)
    employee_joining_date = models.DateField(blank=True, null=True)
    employee_leaving_date = models.DateField(blank=True, null=True)
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
'''

'''
	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
	    return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)  
    def has_module_perms(self, app_label):
		return True
'''

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    buildingNumber = models.CharField(max_length=100, null=True, blank=True)
    buildingName  = models.CharField(max_length=100, null=True, blank=True)
    steetNumber = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True) #another name is state
    zip = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length = 100, null=True, blank=True)
    belongs_to = models.ManyToManyField(User, null=True, blank=True)
    is_personal = models.BooleanField(default=False)#if not personal then it is a public address, therefore, anyone can see it
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



<<<<<<< Updated upstream
=======
class Client(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
>>>>>>> Stashed changes

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.buildingNumber, self.buildingName, self.steetNumber, self.street, self.city, self.belongs_to)
        #return self.buildingNumber + " " + self.buildingName + " " + self.steetNumber + " " + self.city + " " + self.zip

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.name


<<<<<<< Updated upstream
class JobCard(models.Model):
    id = models.AutoField(primary_key=True)
    job_card_number = models.CharField(max_length=100, null=True, blank=True)#unique for every company
    job_card_client = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='job_card_client')
    #job_card_client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #job_card_requester might be making this redundant
=======
class Employee(models.Model):
    #before production, remember to accomodate for users in other countries
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id_num = models.CharField(max_length=13, unique=False)
    employee_name = models.CharField(max_length=50, null=True, blank=True)
    employee_phone = models.CharField(max_length=10, null=True, blank=True)
    employee_address = models.CharField(max_length=100, null=True, blank=True)
    employee_designation = models.CharField(max_length=50, null=True, blank=True)
    employee_joining_date = models.DateField(blank=True, null=True)
    employee_leaving_date = models.DateField(blank=True, null=True)
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.employee_name

class JobCard(models.Model):
    id = models.AutoField(primary_key=True)
    job_card_number = models.CharField(max_length=100, null=True, blank=True)#unique for every company
    job_card_client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True) #job_card_requester might be making this redundant
>>>>>>> Stashed changes
    job_card_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    job_card_reference = models.CharField(max_length=100, null=True, blank=True)#can include invoice number or PO number
    job_card_location = models.CharField(max_length=100, null=True , blank=True) # department
    job_card_created_at = models.DateTimeField(auto_now_add=True)
    job_card_started_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    job_card_completed_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    job_card_employees = models.ManyToManyField(User, blank=True)
    job_card_category = models.ForeignKey('JobCardCategory', on_delete=models.CASCADE, null=True, blank=True)
    job_card_status_options = [(1,'New'), (2,'Accepted'), (3,'Travelling to Site'), (4,'In Progress'), (5,'Paused'),  (6,'Completed'), (7,'Cancelled')]
    job_card_status = models.IntegerField(null=True, blank=True, choices=job_card_status_options, default=1)
    job_card_description = models.TextField(null=True, blank=True)
    priotiry_data = [(1,'Low'), (2,'Normal'), (3,'High')]
    job_card_priority = models.IntegerField(choices=priotiry_data, default=2)
    job_card_resolution = models.TextField(null=True, blank=True)
    job_card_completion_description = models.CharField(max_length=100, null =True, blank=True)
    job_card_last_pause = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    job_card_nva_time = models.DurationField(null=True, blank=True)#describes the time in which nothing was done. Will be done in the frontend
    job_card_requester = models.ForeignKey('ClientUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.job_card_number or 'No Job Card Number'


class JobCardCategory(models.Model):
    id = models.AutoField(primary_key=True)
    company_owner = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True) #to show which company owns this category
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    #owned_by = models.ManyToManyField('Company', blank=True)
    def __str__(self):
        return self.name



class ClientUser(models.Model): #different users in each organization. They request jobs in the organization   
    id = models.AutoField(primary_key=True)
<<<<<<< Updated upstream
    works_for = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
=======
    works_for = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
>>>>>>> Stashed changes
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class MaterialUsed(models.Model):
    material_name = models.CharField(max_length=100, null=True, blank=True)
    material_barcode = models.CharField(max_length=100, null=True, blank=True)	
    material_quantity = models.IntegerField(null=True, blank=True)
    material_unit = models.CharField(max_length=100, null=True, blank=True)
    material_price = models.IntegerField(null=True, blank=True)
    material_remarks = models.CharField(max_length=100, null=True, blank=True)
    material_job = models.ForeignKey('JobCard', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.material_name


<<<<<<< Updated upstream

'''
from iSmartcoApp.utils import (generateNextClientNumber,
                               generateNextEmployeeNumber,
                               generateNextJobCardNumber)
=======
#function for creating job card number
def generateNextJobCardNumber(company_id):
    nextNum = JobCard.objects.filter(job_card_company=company_id).count()#find a much more effective way. lets say there's 10 job. and [5] gets deleted. this thing will count 9 jobs and make a job number 10. therefore, theres no uniqueness.  
    nextNum += 1
    return nextNum
>>>>>>> Stashed changes


@receiver(post_save, sender=User)

@receiver(post_save, sender=Client)
def create_client_number(sender, instance, created, **kwargs):
    if created:
        instance.client_number = generateNextClientNumber(company_id = instance.job_card_company.id)
        instance.save()

@receiver(post_save, sender=JobCard)
# Now Creating a Function which will automatically insert data into the JobCard table
def create_Job_Card_Number(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        nextNum = generateNextJobCardNumber(company_id = instance.job_card_company.id)
        instance.job_card_number = nextNum
        instance.save()

<<<<<<< Updated upstream
'''
'''
=======


>>>>>>> Stashed changes
@receiver(post_save, sender=User)
#Creating a function which will automatically insert data into the Employee or client table
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 3:
<<<<<<< Updated upstream
            User.objects.create(id=instance, name=instance.first_name)
=======
            Client.objects.create(id=instance, name=instance.first_name)
>>>>>>> Stashed changes
        elif instance.user_type == 2 or instance.user_type == 4:
            Employee.objects.create(id=instance)
            #created_by = Company.objects.get(created_by=instance.email)
        elif instance.user_type == 1:
            pass
'''
'''
@receiver(post_save, sender=User)
#creating a finction to save the data into in the instance
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 3:
        instance.client.save()
    elif instance.user_type == 2 or instance.user_type == 4:
        instance.employee.save()
    elif instance.user_type == 1:
        pass
'''
'''
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
'''
