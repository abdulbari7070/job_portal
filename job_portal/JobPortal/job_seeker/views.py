from django.shortcuts import render
from employer.models import Job


def dashboard(request):
    jobs = Job.objects.all() 
    return render(request, 'job_seeker/dashboard.html', {'jobs': jobs})