from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployerRegistrationForm, EmployerProfileForm, JobForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy


from django.contrib.auth.views import LogoutView
from .models import Job, EmployerProfile

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy

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


# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('employer:employer_login')
#     job_count = Job.objects.filter(employer=request.user).count()
#     jobs = Job.objects.filter(employer=request.user) 
#     # Job Application is static for now 
#     return render(request, 'employer/dashboard.html', {'job_count': job_count, 'job_application_count': 9, 'jobs': jobs})

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'employer/dashboard.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_count'] = self.get_queryset().count()
        # Job Application count is static for now
        context['job_application_count'] = 9
        return context


# def post_job(request):
#     if not request.user.is_authenticated:
#         return redirect('employer:employer_login')

#     if request.method == 'POST':
#         form = JobForm(request.POST)
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.employer = request.user
#             job.save()
#             return redirect('employer:employer_dashboard') 
#     else:
#         form = JobForm()
#     return render(request, 'employer/post_job.html', {'form': form})


class PostJobView(LoginRequiredMixin, CreateView):
    template_name = 'employer/post_job.html'
    form_class = JobForm
    success_url = reverse_lazy('employer:employer_dashboard')

    def form_valid(self, form):
        job = form.save(commit=False)
        job.employer = self.request.user
        return super().form_valid(form)


# def edit_job(request, job_id):
#     if not request.user.is_authenticated:
#         return redirect('employer:employer_login')

#     job = Job.objects.get(pk=job_id)
#     if request.method == 'POST':
#         form = JobForm(request.POST, instance=job)
#         if form.is_valid():
#             form.save()
#             return redirect('employer:employer_dashboard') 
#     else:
#         form = JobForm(instance=job)
#     return render(request, 'employer/edit_job.html', {'form': form})

class EditJobView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'employer/edit_job.html'
    success_url = reverse_lazy('employer:employer_dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(employer=self.request.user)


# def delete_job(request, job_id):
#     if not request.user.is_authenticated:
#         return redirect('employer:employer_login')

#     job = get_object_or_404(Job, pk=job_id)
#     if request.method == 'POST':
#         job.delete()
#         return redirect('employer:employer_dashboard') 
#     return render(request, 'employer/delete_job.html', {'job': job})
    
class DeleteJobView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'employer/delete_job.html'
    success_url = reverse_lazy('employer:employer_dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(employer=self.request.user)