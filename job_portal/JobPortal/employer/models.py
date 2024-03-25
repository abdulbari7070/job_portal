from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model


User = get_user_model()

class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.ManyToManyField(Skill)
    experience_required = models.CharField(max_length=50)  
    employer = models.ForeignKey(User, on_delete=models.CASCADE) 

    @property
    def skills_list(self):
        return ', '.join(skill.name for skill in self.skills_required.all())

    def __str__(self):
        return self.title
    
    @property
    def experience_years_months(self):
        years = int(self.experience_required) // 12
        months = int(self.experience_required) % 12
        return f"{years} years, {months} months"
