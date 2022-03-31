from rest_framework import serializers

from iSmartcoApp.models import JobCard, Employee, Company, Client, User


class RegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}	


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

	def get_company_name_from_JobCard(self, job_card):
		return job_card.company.company_name

	def get_last_job_card_number(self, job_card):
		return job_card.last_job_card_number
 
	def get_client_name_from_Client(self, job_card):
		return job_card.client.client_name

	def get_employee_name_from_Employee(self, job_card):
		return job_card.employee.employee_name

	class Meta:
		model = JobCard
		fields = '__all__'




