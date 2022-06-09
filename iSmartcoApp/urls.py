from iSmartcoApp import views
from django.urls import include, re_path

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    re_path(r'^JobCardApi$',views.JobCardApi),
    re_path(r'^EmployeeApi$',views.EmployeeApi),	
    re_path(r'^CompanyApi$',views.CompanyApi),
    re_path(r'^ClientApi$',views.ClientApi),
    re_path(r'^RegisterApi$', views.RegisterApi),
    re_path(r'^LoginApi$', views.LoginApi), #might need .as_view()
    re_path(r'^LogoutApi$', views.LogoutApi),
    re_path(r'^current_user$', views.current_user),
<<<<<<< Updated upstream
    re_path(r'^create_client_user$', views.create_client_user),
    re_path(r'^JobCardCategoryApi$', views.JobCardCategoryApi),
    re_path(r'^Job_Card/start_job_card$', views.start_job_card),
    re_path(r'^Job_Card/pause_job_card$', views.pause_job_card),
    re_path(r'^Job_Card/continue_job_card$', views.continue_job_card),
    re_path(r'^Job_Card/complete_job_card$', views.complete_job_card),
    re_path(r'^Job_Card/cancel_job_card$', views.cancel_job_card),
=======
>>>>>>> Stashed changes
]