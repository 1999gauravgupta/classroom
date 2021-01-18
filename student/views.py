from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Submission


class SubmissionListView(LoginRequiredMixin,ListView):
    model=Submission
    template_name = 'student_home.html'

@login_required
def student_home(request):
    return render(request,'student_home.html')

def register_student(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            return redirect('student_home')
    else:
        form = UserRegisterForm()
    return render(request, 'register_student.html', {'form': form})

@login_required
def create_submission(request):
    return render(request,'create_submission.html')

@login_required
def update_submission(request,id):
    return render(request,'update_submission.html')

@login_required
def delete_submission(request,id):
    return render(request,'delete_submission.html')

@login_required
def report_submission(request,id):
    return render(request,'report_submission.html')

def student_logout(request):
    logout(request)
    return redirect('core_home')