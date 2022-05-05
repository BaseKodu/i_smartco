from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user, get_user_model


from iSmartcoApp.models import (Client, Company, Employee, JobCard,
                                JobCardCategory, MaterialUsed, User)
from iSmartcoApp.utils import (getClients)		




class UserSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	first_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
	last_name = serializers.CharField(required=False, allow_blank=True, max_length=100)
	email = serializers.EmailField(required=False, allow_blank=True, max_length=100)
	#username = serializers.CharField(required=False, allow_blank=True, max_length=100)
	#password = serializers.CharField(required=False, allow_blank=True, max_length=100)
	is_active = serializers.BooleanField(required=False)
	#is_staff = serializers.BooleanField(required=False, allow_blank=True)
	#is_superuser = serializers.BooleanField(required=False, allow_blank=True)
	#last_login = serializers.DateTimeField(required=False, allow_blank=True)
	date_joined = serializers.DateTimeField(required=False)
	user_company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)

	
	class Meta:
		model = User
		fields = ['id','first_name', 'last_name', 'email', 'is_active', 'date_joined', 'user_company']

	def getCurrentUser(self):
		return self.context['request'].user
	


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False, write_only=True)
    # This will be used when the DRF browsable API is enabled

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: User does not exist'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):

	#adding two extra fields
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	company_name = serializers.CharField(style={'input_type' : 'text'}, required=True)

	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'password2', 'company_name', 'user_type']
		extra_kwargs = {
				'password': {'write_only': True}, #dont want anyone to see the password
				'company_name': {'write_only': False}
		}	

	def	save(self):

		#in this save function we will be creating a user and a company record. a user, which by default will be CompAdmin, will get the pk of the company he just created. 

		user = User(
					#creating a user record. it will record company fk
					email=self.validated_data['email'],
					username=self.validated_data['username'],
					#user_company=self.post_to_company(),
				)

		company = Company(
						#creating a company record.
						name=self.validated_data['company_name'],
						user=self.instance,
						#created_by = self.validated_data['email']
					)

		#validating the password
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2: #trying to match passwords. Other validation, ie valid characters, will be done by django automatically
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		
		user.set_password(password) #setting the password
		company.save() #saving the company
		user.user_company = company #setting the company fk
		user.save() #saving the user
		return user

#curr_User_Company = User.user_company.id

class ClientSerializers(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	client_name = serializers.CharField(style={'input_type' : 'text'}, required=True)


	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'password2', 'user_type', 'client_name']	
		extra_kwargs = {
				'password': {'write_only': True}, #dont want anyone to see the password
				'user_type': {'read_only': True},
		}

	
	def	save(self):
		user = User(
					#creating a user record. it will record company fk
					email=self.validated_data['email'],
					username=self.validated_data['username'],
					user_type = 3,
					first_name = self.validated_data['client_name'],)
					#user_company = get_user(self.request).user_company)
					

		
		#validating the password
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:	#trying to match passwords.
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		
		user.set_password(password) #setting the password
		user.save() #saving the user
		return user

		


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
	
	#this is brilliant. Dont remove it.
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



	class Meta:
		model = JobCard
		fields = '__all__'
		#fields = ['job_card_number', 'job_card_reference', 'job_card_status', 'job_card_description', 'company_name', 'client_name', 'employee']/
		extra_kwargs = {
				'job_card_number': {'read_only': True},
				'password': {'write_only': True},
				'company_name': {'write_only': False},
				#'job_card_number': {'read_only': True}
		}
	
	
	#I want to restrict users to see to clent info based on their client type. if client_type=1:see all clients. if client_type=2:see only clients that are assigned to them. if client_type=3:see only clients themselves. if client_type=4, see clients.
	#jc_client = getClients()

	UserType = User.user_type
	UserCompany = User.user_company
	print(f'UserCompany is {UserCompany}')
	objClients = getClients(UserType, UserCompany)

	def save(self):
		job_card = JobCard(
							job_card_reference = self.validated_data['job_card_reference'],
							job_card_status = self.validated_data['job_card_status'],
							job_card_description = self.validated_data['job_card_description'],
							job_card_technicians = self.validated_data['job_card_technicians'],
							job_card_company = self.validated_data['job_card_company'],
							job_card_client = self.validated_data['job_card_client'],
							job_card_started_at = self.validated_data['job_card_started_at'],
							job_card_completed_at = self.validated_data['job_card_completed_at'],
							job_card_priority = self.validated_data['job_card_priority'],
							job_card_category = self.validated_data['job_card_category'],
						)
		
		#validating if user can see client data
		job_card_client = self.validated_data['job_card_client']
		try :
			if self.UserType ==2 or self.UserType ==4 and job_card_client in self.objClients: # if user_type is compadmin and employee they shoulb be able to see all company clients
				job_card.job_card_client = self.validated_data['job_card_client']
			elif self.UserType ==3 and job_card_client == self.objClients:
				job_card.job_card_client = self.validated_data['job_card_client']
			job_card.save() #saving the job_card
			return job_card
		except :
			raise serializers.ValidationError({'job_card_client': 'You are not authorized to create a job card for client.'})

