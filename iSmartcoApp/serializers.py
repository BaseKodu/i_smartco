from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver

from iSmartcoApp.models import (Client, Company, Employee, JobCard,
                                JobCardCategory, MaterialUsed, User)


class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	company_name = serializers.CharField(style={'input_type' : 'text'}, required=True)

	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'password2', 'company_name']
		extra_kwargs = {
				'password': {'write_only': True},
				'company_name': {'write_only': False}
		}	

	def post_to_company(self):
		company = Company(
						name=self.validated_data['company_name'],
						user=self.instance,
						created_by = self.validated_data['email']
					)
		company.save()

		


	def	save(self):

		user = User(
					email=self.validated_data['email'],
					username=self.validated_data['username']
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		user.set_password(password)
		user.save()
		return user

		#check denis ivy for payment stuff
		template = render_to_string('templates/email_template.html', {request.user.username})
		email = EmailMessage('Welcome to iSmartco', 
							 'Thank you for registering with us.',
							 settings.EMAIL_HOST_USER,
							 to=[self.validated_data['email']])



class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CompanySerializers(serializers.ModelSerializer):

	
	class Meta:
		model = Company
		fields = '__all__'
		
	


class EmployeeSerializers(serializers.ModelSerializer):

	get_total_employees = serializers.SerializerMethodField('get_total_employees')
	def get_total_employees(self, *args, **kwargs):
		employee_company = kwargs.get('employee_company', None)
		return Employee.objects.filter(employee_company= employee_company).count()


	class Meta:
		model = Employee
		fields = '__all__'


'''
class CommonFunctions:

	def get_total_employees(self, *args, **kwargs):
		employee_company = kwargs.get('employee_company', None)
		return Employee.objects.filter(employee_company= employee_company).count()

	def generateJobCardNumber(self, last_job_card_number):
		last_job_card_number += 1
		return last_job_card_number
'''

	

class JobCardSerializers(serializers.ModelSerializer):
	
	
	#for displaying
	#total_num_of_jobs = serializers.SerializerMethodField('get_total_num_of_jobs')
	def total_num_of_jobs(self, *args, **kwargs): #test properly when theres a lot of data in the table
		#some filters wont be added to the query
		#view jobs by company, employee, client, status, category, date
		company_id = kwargs.get('company_id', None)
		category_id = kwargs.get('category_id', None)
		employee_id = kwargs.get('employee_id', None)
		client_id = kwargs.get('client_id', None)
		date_started = kwargs.get('date_started', None)
		date_completed = kwargs.get('date_completed', None)
		job_card_status = kwargs.get('job_card_status', None)
		priority = kwargs.get('priority', None)
		return JobCard.objects.filter(job_card_company=company_id, job_category=category_id, job_card_technicians=employee_id, job_card_client=client_id, job_card_started_at=date_started, job_card_completed_at=date_completed, job_card_status=job_card_status, job_card_priority=priority).count()



	#get_job_card_category = serializers.SerializerMethodField('get_job_card_category')
	def get_job_card_category(self, job_card):
		company_categories = JobCardCategory.objects.filter(owned_by=job_card.job_card_company)
		return company_categories.id


	

	#company_name = serializers.SerializerMethodField('get_company_name_from_JobCard')	
	def get_company_name_from_JobCard(self, job_card):
		return job_card.job_card_company#.name

	#client_name = serializers.SerializerMethodField('get_client_name_from_Client')
	def get_client_name_from_Client(self, job_card):
		return job_card.job_card_client#.name

	'''employee = serializers.SerializerMethodField('get_employee_name_from_Employee')
	def get_employee_name_from_Employee(self, job_card):
		return job_card.job_card_technicians#.employee_name'''


	class Meta:
		model = JobCard
		fields = '__all__'
		#fields = ['job_card_number', 'job_card_reference', 'job_card_status', 'job_card_description', 'company_name', 'client_name', 'job_card_client', 'job_card_company']
		extra_kwargs = {
				'job_card_number': {'read_only': True},
				'password': {'write_only': True},
				'company_name': {'write_only': False}
		}


	def post_to_job_card(self):
		job_card = JobCard(
							job_card_client= self.validated_data['job_card_client'],
							job_card_company= self.validated_data['job_card_company'],
							job_card_reference = self.validated_data['job_card_reference'],
							job_card_technicians = self.validated_data['job_card_technicians'],
							job_card_status = self.validated_data['job_card_status'],
							job_card_description = self.validated_data['job_card_description'],
							job_card_priority = self.validated_data['job_card_priority'],
							job_card_resolution = self.validated_data['job_card_resolution'],
							job_card_completion_description = self.validated_data['job_card_completion_description'],
							job_card_requester = self.validated_data['job_card_requester'],
							job_category=self.validated_data['category_id']
							)
		job_card.save()
		return job_card


class JobCardCategory(serializers.ModelSerializer):
	class Meta:
		model = JobCard
		fields = ['category']
		


class UserSerializers(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'
		

	get_company_clients = serializers.SerializerMethodField('get_company_clients_from_User')#try making for all users
	def get_company_clients_from_User(self, *args, **kwargs):
		company_id = kwargs.get('company_id', None)
		user_type = kwargs.get('user_type', None)
		return User.objects.filter(user_type=user_type, user_company=company_id).count()


