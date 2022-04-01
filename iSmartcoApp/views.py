from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from iSmartcoApp.models import JobCard, Employee, Company, Client, User
from iSmartcoApp.serializers import JobCardSerializers, EmployeeSerializers, CompanySerializers, ClientSerializers, RegistrationSerializer

# Create your views here.

@csrf_exempt
def RegisterApi(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = RegistrationSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			serializer.post_to_company()
			return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






'''
	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			user = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = user.email
			data['username'] = user.username
			status = 201
		else:
			data = serializer.errors
			status = 400
		return JsonResponse(data, status=status)

'''

@csrf_exempt
def ClientApi(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = ClientSerializers(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
	elif request.method == 'GET':
		client = Client.objects.all()
		serializer = ClientSerializers(client, many=True)
		return JsonResponse(serializer.data, safe=False)
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = ClientSerializers(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
	
	



@csrf_exempt
def CompanyApi(request): #could very well prove to be unnecessary
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CompanySerializers(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'GET':
		companies = Company.objects.all()
		serializer = CompanySerializers(companies, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CompanySerializers(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)


#create job card
@csrf_exempt
def JobCardApi(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = JobCardSerializers(data=data)
		last_job_card_number = serializer.get_last_job_card_number() + 1
		if serializer.is_valid():
			serializer.save()
			serializer.last_job_card_number = last_job_card_number
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
	
	elif request.method == 'GET':
		job_card = JobCard.objects.all()
		serializer = JobCardSerializers(job_card, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		job_card = JobCard.objects.get(id=data['id'])
		serializer = JobCardSerializers(job_card, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)
		

#create employee
@csrf_exempt
def EmployeeApi(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = EmployeeSerializers(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
	
	elif request.method == 'GET':
		employee = Employee.objects.all()
		serializer = EmployeeSerializers(employee, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		employee = Employee.objects.get(id=data['id'])
		serializer = EmployeeSerializers(employee, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)