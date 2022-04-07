from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import serializers

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


class JobCardSerializers(serializers.ModelSerializer):
	
	
	#for displaying
	total_num_of_jobs = serializers.SerializerMethodField('get_total_num_of_jobs')
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



	get_job_card_category = serializers.SerializerMethodField('get_job_card_category')
	def get_job_card_category(self, job_card):
		company_categories = JobCardCategory.objects.filter(owned_by=job_card.job_card_company)
		return company_categories.id


	get_last_job_card_number = serializers.SerializerMethodField('get_last_job_card_number')
	def get_last_job_card_number(self, job_card, company_id):#ensures every company gets a unique job card number that isnt id
		last_job_card_number = JobCard.objects.filter(company_id=company_id).last()
		return last_job_card_number.job_card_number

	company_name = serializers.SerializerMethodField('get_company_name_from_JobCard')	
	def get_company_name_from_JobCard(self, job_card):
		return job_card.company.company_name

	get_client_name = serializers.SerializerMethodField('get_client_name_from_Client')
	def get_client_name_from_Client(self, job_card):
		return job_card.client.id

	get_employee_name = serializers.SerializerMethodField('get_employee_name_from_Employee')
	def get_employee_name_from_Employee(self, job_card):
		return job_card.employee.id


	class Meta:
		model = JobCard
		#fields = '__all__'
		fields = ['email', 'username', 'password', 'password2', 'company_name']
		extra_kwargs = {
				'password': {'write_only': True},
				'company_name': {'write_only': False}
		}


	def post_to_JobCard(self, validated_data):
		job_card = JobCard(
							#job_card_number= get_last_job_card_number(job_card), needs to be done on  --> models.py
							job_card_client=validated_data['client_id'],
							job_card_company=validated_data['company_id'],
							job_card_reference = validated_data['reference'],
							technicians = validated_data['technicians'],
							job_card_status = validated_data['job_card_status'],
							job_card_description = validated_data['job_card_description'],
							job_card_priority = validated_data['job_card_priority'],
							job_card_resolution = validated_data['job_card_resolution'],
							job_card_completion_description = validated_data['job_card_completion_description'],
							job_card_requester = validated_data['job_card_requester'],
							job_category=validated_data['category_id'],
							job_card_description=validated_data['job_card_description'],
						)
		job_card.save()
		return job_card.id, job_card.job_card_company

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

