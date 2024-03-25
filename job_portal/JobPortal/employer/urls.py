from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = "employer"


urlpatterns = [
    path('login/', views.user_login, name='employer_login'),
    path('register/', views.employer_registration, name='employer_register'),
    path('dashboard/', views.dashboard, name='employer_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # path('post-job/', views.post_job, name='post_job'),
    path('post-job/', views.PostJobView.as_view(), name='post_job'),

    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),




]
