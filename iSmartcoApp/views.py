from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from iSmartcoApp.models import JobCard
from iSmartcoApp.serializers import JobCardSerializers

# Create your views here.


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
		