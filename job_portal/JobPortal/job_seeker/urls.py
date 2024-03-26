from django.urls import path
# from django.views.generic.base import TemplateView
from . import views


app_name = "job_seeker"

urlpatterns = [
    # path('login/', views.user_login, name='job_seeker_login'),
    # path('register/', views.job_seeker_registration, name='job_seeker_register'),
    path('dashboard/', views.dashboard, name='job_seeker_dashboard'),
]
