from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,SubmissionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Submission
from os import path
import os
# from django.core.urlresolvers import reverse


@login_required
def student_home(request):
    submissions=Submission.objects.filter(student=request.user)
    return render(request,'student_home.html',{'submissions':submissions})

def register_student(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            messages.success(request,f'Account created for {username}')
            return redirect('student_home')
    else:
        form = UserRegisterForm()
    return render(request, 'register_student.html', {'form': form})

@login_required
def create_submission(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student=request.user
            obj.save()
            messages.success(request,'Submission successful')
            return redirect('student_home')
    else:
        form = SubmissionForm()
    return render(request, 'create_submission.html', {'form': form})

@login_required
def update_submission(request,id):
    if request.method == 'POST':
        obj = get_object_or_404(Submission, id = id) 
        form = SubmissionForm(request.POST,request.FILES,instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student=request.user
            obj.save()
            messages.success(request,'Submission update successful')
            return redirect('student_home')
    else:
        form = SubmissionForm()
    return render(request, "update_submission.html", {'form': form}) 
    
@login_required
def delete_submission(request,id):
    context ={} 
    obj = get_object_or_404(Submission, id = id) 
    if request.method =="POST": 
        obj.delete() 
        messages.success(request,'Submission deleted')
        return redirect('student_home')  
    return render(request,'delete_submission.html',context)

@login_required
def report_submission(request,id):
    obj=get_object_or_404(Submission,id=id)
    report=f'files/{obj.assignment.subject}/{obj.assignment.name}/report.txt'
    flag=False
    marks=None
    mean=None
    median=None
    minimum=None
    maximum=None
    total=None
    range=None
    if path.exists(report):
        if os.stat(report).st_size>0:
            fh=open(report)
            contents = fh.read()
            contents = contents.splitlines()
            for line in contents:
                if line.startswith(obj.file.name):
                    marks=float(line[line.index("=")+1:])
                    flag=True
                elif line.startswith("mean"):
                    mean=float(line[line.index("=")+1:])
                elif line.startswith("median"):
                    median=float(line[line.index("=")+1:])
                elif line.startswith("minimum"):
                    minimum=float(line[line.index("=")+1:])
                elif line.startswith("maximum"):
                    maximum=float(line[line.index("=")+1:])
                elif line.startswith("total"):
                    total=float(line[line.index("=")+1:])
    if flag:
        range=maximum-minimum
    context={"flag":flag,"marks":marks,"mean":mean,"median":median,"minimum":minimum,"maximum":maximum,"total":total,"range":range}
    return render(request,'report_submission.html',context)

def student_logout(request):
    logout(request)
    return redirect('core_home')