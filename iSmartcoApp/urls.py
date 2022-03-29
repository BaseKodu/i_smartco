from iSmartcoApp import views
from django.urls import include, re_path

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    re_path(r'^JobCardApi$',views.JobCardApi),
    re_path(r'^EmployeeApi$',views.EmployeeApi),	
]