from rest_framework import serializers

from iSmartcoApp.models import JobCard, Employee, Company, Client, User


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




class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class JobCardSerializers(serializers.ModelSerializer):
	company_name = serializers.SerializerMethodField('get_company_name_from_JobCard')
	last_job_card_number = serializers.SerializerMethodField('get_last_job_card_number')
	get_client_name = serializers.SerializerMethodField('get_client_name_from_Client')
	get_employee_name = serializers.SerializerMethodField('get_employee_name_from_Employee')
	total_num_of_jobs = serializers.SerializerMethodField('get_total_num_of_jobs')

	def get_last_job_card_number(self, job_card, company_id):#ensures every company gets a unique job card number that isnt id
		last_job_card_number = JobCard.objects.filter(company_id=company_id).last()
		return last_job_card_number.job_card_number

	def total_num_of_jobs(self, *args, **kwargs): #test properly when theres a lot of data in the table
		#some filters wont be added to the query
		company_id = kwargs.get('company_id', None)
		category_id = kwargs.get('category_id', None)
		employee_id = kwargs.get('employee_id', None)
		client_id = kwargs.get('client_id', None)
		date_started = kwargs.get('date_started', None)
		date_completed = kwargs.get('date_completed', None)
		return JobCard.objects.filter(company_id=company_id, category_id=category_id, employee_id=employee_id, client_id=client_id, date_started=date_started, date_completed=date_completed).count()

		
	def get_company_name_from_JobCard(self, job_card):
		return job_card.company.company_name

	def get_client_name_from_Client(self, job_card):
		return job_card.client.client_name

	def get_employee_name_from_Employee(self, job_card):
		return job_card.employee.employee_name

	class Meta:
		model = JobCard
		fields = '__all__'


class JobCardCategory(serializers.ModelSerializer):
	class Meta:
		model = JobCard
		fields = ['category']
		

