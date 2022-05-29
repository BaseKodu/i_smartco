from django.contrib.auth import login, logout
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

<<<<<<< Updated upstream
from iSmartcoApp.models import Company, JobCard, JobCardCategory, User
=======
from iSmartcoApp.models import Client, Company, Employee, JobCard, User
>>>>>>> Stashed changes
from iSmartcoApp.serializers import *

# Create your views here.


#class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.


@csrf_exempt
@permission_classes([IsAuthenticated])
def start_job(request):
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		job_card = JobCard.objects.get(id=data['id'])
		serializer = JobCardSerializers(job_card, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
	#permission_classes = (permissions.IsAuthenticated,)
	serializer = UserSerializer(request.user)
	return Response(serializer.data)

@csrf_exempt
@permission_classes([IsAuthenticated])
def LogoutApi(request):
	if request.method == 'POST':
		logout(request)
		return JsonResponse({'success': 'Logged out'}, status=status.HTTP_200_OK)
	else:
		return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@permission_classes([AllowAny])
def LoginApi(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = LoginSerializer(data=data)
		if serializer.is_valid():
			user = serializer.validated_data['user']
			login(request, user)
			#token, created = Token.objects.get_or_create(user=user)
			#return JsonResponse({'token': token.key})
			return JsonResponse({'success': 'Logged In' }, status=status.HTTP_202_ACCEPTED)
		return JsonResponse({'error': 'Method not allowed'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@permission_classes([AllowAny])
def RegisterApi(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = RegistrationSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#create job card

@csrf_exempt
@permission_classes([IsAuthenticated])
def JobCardApi(request):
<<<<<<< Updated upstream
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = JobCardSerializers(data=data)
		if serializer.is_valid():
			serializer.save(current_user=request.user)
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


@csrf_exempt
@permission_classes([IsAuthenticated])
def ClientApi(request):
=======
>>>>>>> Stashed changes
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = JobCardSerializers(data=data)
		if serializer.is_valid():
			#serializer.data['user_company'] = user_company
			serializer.save(current_user = request.user)
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
<<<<<<< Updated upstream
			return JsonResponse(serializer.data, status=201) #Warning : serializer.data does not return user_company value. It return null although it it recorded in the database
		return JsonResponse(serializer.errors, status=400)
	

=======
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)
>>>>>>> Stashed changes


@csrf_exempt
@permission_classes([IsAuthenticated])
<<<<<<< Updated upstream
def CompanyApi(request): #could very well prove to be unnecessary
=======
def ClientApi(request):
>>>>>>> Stashed changes
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
	



<<<<<<< Updated upstream
		

#create employee
@csrf_exempt
@permission_classes([IsAuthenticated])
def EmployeeApi(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = EmployeeSerializers(data=data)
		if serializer.is_valid():# raises key error: Groups but records the data in the database. Written in known issues
			serializer.save(current_user = request.user)
=======
@csrf_exempt
def CompanyApi(request): #could very well prove to be unnecessary
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CompanySerializers(data=data)
		if serializer.is_valid():
			serializer.save()
>>>>>>> Stashed changes
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'GET':
<<<<<<< Updated upstream
		employee = Employee.objects.all()
		serializer = EmployeeSerializers(employee, many=True)
=======
		companies = Company.objects.all()
		serializer = CompanySerializers(companies, many=True)
>>>>>>> Stashed changes
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
<<<<<<< Updated upstream
		employee = Employee.objects.get(id=data['id'])
		serializer = EmployeeSerializers(employee, data=data)
=======
		serializer = CompanySerializers(data=data)
>>>>>>> Stashed changes
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
<<<<<<< Updated upstream
=======


		
>>>>>>> Stashed changes



#@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def create_client_user(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = ClientUserSerializer(data=data)
		if serializer.is_valid():
			serializer.save(current_user = request.user)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)



@csrf_exempt
@permission_classes([IsAuthenticated])
def JobCardCategoryApi(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = JobCardCategorySerializer(data=data)
		if serializer.is_valid():
			serializer.save(current_user = request.user)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'GET':
		job_card_category = JobCardCategory.objects.all()
		serializer = JobCardCategorySerializer(job_card_category, many=True)
		return JsonResponse(serializer.data, safe=False)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		job_card_category = JobCardCategory.objects.get(id=data['id'])
		serializer = JobCardCategorySerializer(job_card_category, data=data)
		if serializer.is_valid():
<<<<<<< Updated upstream
			serializer.save(current_user = request.user)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
def start_job_card(request):
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		job_card_obj = JobCard.objects.get(id=data['id'])
		serializer = JobCardSerializers(data=data)
		if serializer.is_valid():
			serializer.update(instance=job_card_obj, action_type=4)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@permission_classes([IsAuthenticated])
def pause_job_card(request):
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = JobCardSerializers(data=data)
		if serializer.is_valid():
			serializer.update(action_type=5)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
def continue_job_card(request):
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = JobCardSerializers(data=data)
		if serializer.is_valid():
			serializer.update(action_type=8)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@permission_classes([IsAuthenticated])
def complete_job_card(request):
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = JobCardSerializers(data=data)
		if serializer.is_valid():
			serializer.update(action_type=6)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@permission_classes([IsAuthenticated])
def cancel_job_card(request):
	if request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = JobCardSerializers(data=data)
		if serializer.is_valid():
			serializer.update(action_type=7)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
=======
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)
>>>>>>> Stashed changes
