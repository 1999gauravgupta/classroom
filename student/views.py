from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,SubmissionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Submission
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
    return render(request,'report_submission.html')

def student_logout(request):
    logout(request)
    return redirect('core_home')