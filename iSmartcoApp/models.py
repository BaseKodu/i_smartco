from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    #user_address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True)
    #if user is CompAdmin then company is the company he belongs to
    #if user is Client then company is the company he is serviced by
    #if user is Employee then company is the company he works for
    #if user is sysAdmin then company is null

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    #objects = MyAccountManager()

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
    phone = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.name


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
    job_card_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    #job_card_client = models.CharField(max_length=100, null=True, blank=True)
    job_card_reference = models.CharField(max_length=100, null=True, blank=True)#can include invoice number or PO number
    job_card_location = models.CharField(max_length=100, null=True , blank=True) # department
    job_card_created_at = models.DateTimeField(auto_now_add=True)
    job_card_started_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    job_card_completed_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    job_card_technicians = models.ManyToManyField(Employee, blank=True)
    #job_card_technician = models.CharField(max_length=100, null=True, blank=True)
    job_card_type = models.CharField(max_length=100, null=True, blank=True)
    job_card_status = models.CharField(max_length=100, null=True, blank=True)
    job_card_description = models.TextField(null=True, blank=True)
    job_card_priority = models.CharField(max_length=100, null=True, blank=True, default='Normal')
    job_card_resolution = models.TextField(null=True, blank=True)
    job_card_completion_description = models.CharField(max_length=100, null =True, blank=True)
    job_card_nva_time = models.TimeField(null=True, blank=True)#describes the time in which nothing was done. Will be done in the frontend
    job_card_requester = models.ForeignKey('ClientUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.job_card_number


class JobCardCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    owned_by = models.ManyToManyField('Company', blank=True)
    def __str__(self):
        return self.name


class ClientUser(models.Model): #different users in each organization. They request jobs in the organization   
    id = models.AutoField(primary_key=True)
    works_for = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    department = models.CharField(max_length=100, null=True, blank=True)
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

    def __str__(self):
        return self.material_name




from iSmartcoApp.utils import generateNextClientNumber

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



@receiver(post_save, sender=User)
#Creating a function which will automatically insert data into the Employee or client table
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 3:
            Client.objects.create(id=instance, name=instance.first_name)
        elif instance.user_type == 2 or instance.user_type == 4:
            Employee.objects.create(id=instance)
            #created_by = Company.objects.get(created_by=instance.email)
        elif instance.user_type == 1:
            pass


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
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
'''