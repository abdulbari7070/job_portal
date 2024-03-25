from django.contrib import admin
from .models import EmployerProfile, Job, Skill


# Register your models here.
admin.site.register(EmployerProfile)
admin.site.register(Job)
admin.site.register(Skill)