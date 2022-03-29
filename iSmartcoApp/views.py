from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from iSmartcoApp.models import JobCard, Employee, Company, Client
from iSmartcoApp.serializers import JobCardSerializers, EmployeeSerializers, CompanySerializers, ClientSerializers

# Create your views here.

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
def CompanyApi(request):
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
		if serializer.is_valid():
			serializer.save()
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
