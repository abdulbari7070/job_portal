from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    name = CharField(_("Name of User"), blank=True, max_length=255)
    EMPLOYER = 'employer'
    JOB_SEEKER = 'job_seeker'
    USER_TYPE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (JOB_SEEKER, 'Job Seeker'),
    ]
    user_type = CharField(max_length=20, choices=USER_TYPE_CHOICES, default=EMPLOYER)

    def get_absolute_url(self):
        return reverse("user:detail", kwargs={"username": self.username})
