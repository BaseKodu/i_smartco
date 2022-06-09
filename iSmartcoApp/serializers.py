from ast import Constant
import datetime
from re import S
from django.conf import settings
from django.core.mail import EmailMessage
from django.forms import RadioSelect
from django.template.loader import render_to_string
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user, get_user_model
from datetime import datetime, timezone




from iSmartcoApp.models import (Company, JobCard,
                                JobCardCategory, MaterialUsed, User, ClientUser, JobCardCategory, Address)




# CONSTANT values


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
	user_type = serializers.IntegerField(required=False)

	
	class Meta:
		model = User
		fields = ['id','first_name', 'last_name', 'email', 'is_active', 'date_joined', 'user_company', 'user_type']
	


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
						#user=self.instance,
						#created_by = self.validated_data['email']
					)

		#validating the password
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2: #trying to match passwords. Other validation, ie valid characters, will be done by django automatically
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		
		user.set_password(password) #setting the password
		company.save() #saving the company
		user.user_company = company #setting the company fk on the user table
		user.save() #saving the user
		return user


class ClientSerializers(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	client_name = serializers.CharField(style={'input_type' : 'text'}, required=True)


	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'password2', 'user_type', 'client_name', 'user_company']	
		extra_kwargs = {
				'password': {'write_only': True}, #dont want anyone to see the password
				'user_type': {'read_only': True},
		}

	
	def	save(self, current_user):
		usr_comp = current_user.user_company
		user = User(
					#creating a user record. it will record company fk
					email=self.validated_data['email'],
					username=self.validated_data['username'],
					user_type = 3,
					first_name = self.validated_data['client_name'],
					user_company = usr_comp)
					

		
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
		#fields = '__all__'
		fields = ['email', 'username', 'password', 'password2', 'user_type', 'company_name', 'user_company']
		
	


class EmployeeSerializers(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	employee_name = serializers.CharField(style={'input_type' : 'text'}, required=False)

	class Meta:
		model = User
		#fields = '__all__'
		fields = ['email', 'username', 'password', 'password2', 'employee_name', 'user_type']
		extra_kwargs = {
				'password': {'write_only': True}, #dont want anyone to see the password
				'user_type': {'read_only': True},
		}

	def	save(self, current_user):
		usr_comp = current_user.user_company #current_user contains the object of logged in user
		user = User(
					#creating a user record. it will record employee fk
					email=self.validated_data['email'],
					username=self.validated_data['username'],
					first_name = self.validated_data['employee_name'],
					user_company = usr_comp,
					user_type = 4,
					created_by = current_user
					)

		
		
		#validating the password
		password = self.validated_data['password']	
		password2 = self.validated_data['password2']
		if password != password2:	#trying to match passwords.
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		
		user.set_password(password) #setting the password
		user.save() #saving the user

	
from iSmartcoApp.utils import (getClients, generateNextJobCardNumber, getClientUsers, Check_if_object_exists, getJobCardCategories, getEmployees, job_card_times_and_statuses )		

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
		#fields = '__all__'
		fields = ['job_card_number', 'job_card_reference', 'job_card_description', 'job_card_client', 'job_card_requester','job_card_category', 'job_card_employees']
		extra_kwargs = {
				'job_card_number': {'read_only': True},
				'job_card_employees':{'required': False},

		}
	
	
		#I want to restrict users to see to clent info based on their client type. if client_type=1:see all clients. 
		#if client_type=2:see only clients that are assigned to them. if client_type=3:see only clients themselves. 
		#if client_type=4, see clients. thank you autopilot :)




		
	def update_times_and_statuses(self, instance, action_type):
		if action_type == 4:
			instance.job_card_status, instance.job_card_started_at = job_card_times_and_statuses(action_type=action_type)
		elif action_type == 5:
			instance.job_card_status, instance.job_card_last_pause = job_card_times_and_statuses(action_type=action_type)
		elif action_type == 8: #for continue
			instance.job_card_status, instance.job_card_nva_time = job_card_times_and_statuses(action_type=action_type, last_pause=instance.job_card_last_pause)
		elif action_type == 6:
			instance.job_card_status, instance.job_card_completed_at = job_card_times_and_statuses(action_type=action_type)
		elif action_type == 7: #for cancel_job
			instance.job_card_status, instance.job_card_completed_at = job_card_times_and_statuses(action_type=action_type)

		instance.save()
		return instance


	def save(self, current_user):
		job_card = JobCard(
							job_card_reference = self.validated_data['job_card_reference'],
							job_card_description = self.validated_data['job_card_description'],
						)

		#Extract the usertype and user company from the current user and assign them to objClients, which will return a list of clients you can work with
		#youll pass these vales to functions in save or utils
		UserType = current_user.user_type
		UserCompany = current_user.user_company
		user_id = current_user.id


		objClients = getClients(UserType, UserCompany, user_id)

	
		#Ensuring that the client selects themselves by default
		if current_user.user_type == 3:
			job_card_client = current_user
		elif current_user.user_type == 2 or current_user.user_type==4:
			job_card_client = self.validated_data['job_card_client']
		#Ensuring that selected Client is in the list of clients you can work with
		Client_exists = Check_if_object_exists(objClients, job_card_client)
		
		list_for_non_existant_employees = []

		#to ensure valid and authorized data is passed and to save the job card object
		print(f'job_card_client is {job_card_client}')
		if job_card_client:
			print(f'job_card_client is {job_card_client}')
			if Client_exists: #if the client is in the list
				print('Client_exists is True')
				#Now ensuring that only the right requester can be picked
				objClientUsers = getClientUsers(job_card_client)
				job_card_requester = self.validated_data['job_card_requester']
				clientUserExists = Check_if_object_exists(objClientUsers, job_card_requester) #check if the user is in the list of users that can be assigned to the client
				if clientUserExists or job_card_requester == None:
					print(f'clientUserExists is {clientUserExists}, job_card_requester is {job_card_requester}')
					'''
					To add the job card category to the job card
					#ensuring that user can only select categories 
					#assigned to company and Genaral Company
					# '''
					category = self.validated_data['job_card_category']
					objCategories = getJobCardCategories(UserCompany)
					jobCategoryExists = Check_if_object_exists(objCategories, category)
					if jobCategoryExists or category == None: 
						job_card.job_card_category = category
						job_card.job_card_requester = job_card_requester #assigning the requester
						job_card.job_card_client = job_card_client #assigning the client
						job_card.job_card_number = generateNextJobCardNumber(company_id = UserCompany) #generating the job card number, unique per company
						job_card.job_card_company = UserCompany # assign the company on the job card
						job_card.save()
						#adding the employees to the job card
						employee_exixts = False
						try: #if theres a value in job_card_employees then we need to add the employees to the job card
							job_card_employees = self.validated_data['job_card_employees']
							objEmployees = getEmployees(UserCompany)
							for emp in job_card_employees:
								employee_exixts = Check_if_object_exists(objEmployees, emp)
								if employee_exixts:
									job_card.job_card_employees.add(emp)
								else:
									list_for_non_existant_employees.append(emp) #find a way to let the user know that some people cannot be selected
							job_card.save()
						except: #if theres no employees then we dont need to add them to the job card
							job_card.save()
						return job_card #return the job card object with employees added this time
					else:
						raise serializers.ValidationError({'job_card_category': 'Not a valid category'})
				else:
					raise serializers.ValidationError({'job_card_requester': 'You are not allowed to work on this client User.'})
			else:
				raise (serializers.ValidationError({'job_card_client': 'You are not authorized to work on this client.'}))
		else:
			raise (serializers.ValidationError({'job_card_client': 'Please select a client.'}))


class ClientUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = ClientUser
		fields = ['first_name', 'last_name', 'email', 'department', 'works_for']

	def save(self, current_user):
		client_user = ClientUser(
							first_name = self.validated_data['first_name'],
							last_name = self.validated_data['last_name'],
							email = self.validated_data['email'],
							department = self.validated_data['department'],
							#phone and address youll see later
		)

		UserType = current_user.user_type
		UserCompany = current_user.user_company
		user_id = current_user.id
		objClients = getClients(UserType, UserCompany, user_id)
		print(f'objClients is {objClients} \nUserType is {UserType} \nUserCompany is {UserCompany} \nuser_id is {user_id}')


		
		#Ensuring that the client selects themselves by default
		client = self.validated_data['works_for']
		if current_user.user_type == 3:
			client = current_user
		elif current_user.user_type == 2 or current_user.user_type==4:
			client = self.validated_data['works_for']

		exists = False
		for cl in objClients:
			if cl == client:
				exists = True
				print(f'{client} is on the list of clients you can work with')
	
		if client:
			if exists:
				client_user.works_for = client
				client_user.save()
				return client_user
			else:
				#client_user.delete()
				raise (serializers.ValidationError(detail={'client': 'You are not authorized to work on this client.'}, code = 400))
		else:
			raise (serializers.ValidationError(detail={'client': 'Please select a client.'}, code = 400))





class JobCardCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = JobCardCategory
		fields = ['name', 'description']

	def save(self, current_user):
		job_card_category = JobCardCategory(
							name = self.validated_data['name'],
							description = self.validated_data['description'],
		)
		company_owner = current_user.user_company
		job_card_category.company_owner = company_owner
		job_card_category.save()
		return job_card_category


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['buildingNumber', 'buildingName', 'steetNumber', 'street', 'city', 'province', 'zip', 'country', 'belongs_to', 'is_personal', 'is_primary']

	def save(self, current_user):
		address = Address(
							buildingNumber = self.validated_data['buildingNumber'],
							buildingName = self.validated_data['buildingName'],
							steetNumber = self.validated_data['steetNumber'],
							street = self.validated_data['street'],
							city = self.validated_data['city'],
							province = self.validated_data['province'],
							zip = self.validated_data['zip'],
							country = self.validated_data['country'],
							is_personal = self.validated_data['is_personal'],
							is_primary = self.validated_data['is_primary'],
							belongs_to = self.validated_data['belongs_to'],
		)


		address.save()
		return address