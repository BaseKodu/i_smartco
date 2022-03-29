from rest_framework import serializers

from iSmartcoApp.models import JobCard, Employee, Company, Client



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
    class Meta:
        model = JobCard
        fields = '__all__'

