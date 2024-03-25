from django import forms
from django.contrib.auth import get_user_model
from django import forms
from .models import EmployerProfile, Job



User = get_user_model()

class EmployerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password']

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name']

class ExperienceField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(min_value=0),  # Years
            forms.IntegerField(min_value=0),  # Months
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            years, months = data_list
            return years * 12 + months
        return None

class ExperienceFormField(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        widgets = (
            forms.NumberInput(attrs={'placeholder': 'Years'}),
            forms.NumberInput(attrs={'placeholder': 'Months'}),
        )
        super().__init__(widgets, *args, **kwargs)

    def decompress(self, value: int):        
        if value:
            value = int(value)
            years = value // 12
            months = value % 12
            return [years, months]
        return [None, None]


class ExperienceFieldForm(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(min_value=0),  # Years
            forms.IntegerField(min_value=0),  # Months
        )
        super().__init__(
            fields,
            widget=ExperienceFormField(),
            *args,
            **kwargs
        )

    def compress(self, data_list):
        if data_list:
            years, months = data_list
            return years * 12 + months
        return None


class JobForm(forms.ModelForm):
    experience_required = ExperienceFieldForm(required=True)

    class Meta:
        model = Job
        fields = ['title', 'description', 'skills_required', 'experience_required']


