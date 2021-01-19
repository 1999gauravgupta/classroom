from student.models import Submission
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Submission

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model=Submission
        fields=['assignment','file']