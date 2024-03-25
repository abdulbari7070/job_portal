from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployerRegistrationForm, EmployerProfileForm, JobForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy


from django.contrib.auth.views import LogoutView
from .models import Job, EmployerProfile

from django.contrib.auth import get_user_model


User = get_user_model()

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('employer:employer_dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('employer:employer_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'employer/employer_login.html', {'form': form})


def employer_registration(request):
    if request.user.is_authenticated:
        return redirect('employer:employer_dashboard')

    if request.method == 'POST':
        user_form = EmployerRegistrationForm(request.POST)
        profile_form = EmployerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('employer:employer_dashboard')  
    else:
        user_form = EmployerRegistrationForm()
        profile_form = EmployerProfileForm()
    return render(request, 'employer/employer_register.html', {'user_form': user_form, 'profile_form': profile_form})


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('employer:employer_login')

    user_id =  request.user.id
    user = User.objects.get(pk=user_id)
    employer_profile = EmployerProfile.objects.get(user=user)

    if request.method == 'POST':    
        user_form = EmployerRegistrationForm(request.POST, instance=user)
        user_form.fields.pop('password')
        profile_form = EmployerProfileForm(request.POST, instance=employer_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            password = request.POST.get('password')
            if password:
                user.set_password(password)
            user.save()
            profile = profile_form.save()
            return redirect('employer:employer_dashboard')
    else:
        user_form = EmployerRegistrationForm(instance=user)
        del user_form.fields['password']

        profile_form = EmployerProfileForm(instance=employer_profile)
    return render(request, 'employer/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('employer:employer_login')
    job_count = Job.objects.filter(employer=request.user).count()
    jobs = Job.objects.filter(employer=request.user) 
    # job_application_count = JobApplication.objects.filter(job__employer=request.user).count()
    return render(request, 'employer/dashboard.html', {'job_count': job_count, 'job_application_count': 15, 'jobs': jobs})


def post_job(request):
    if not request.user.is_authenticated:
        return redirect('employer:employer_login')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('employer:employer_dashboard') 
    else:
        form = JobForm()
    return render(request, 'employer/post_job.html', {'form': form})


def edit_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('employer:employer_login')

    job = Job.objects.get(pk=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer:employer_dashboard') 
    else:
        form = JobForm(instance=job)
    return render(request, 'employer/edit_job.html', {'form': form})


def delete_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('employer:employer_login')

    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('employer:employer_dashboard') 
    return render(request, 'employer/delete_job.html', {'job': job})