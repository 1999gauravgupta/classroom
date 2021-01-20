from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from .models import Assignment
from .forms import AssignmentForm
from django.contrib import messages
from os import path
import os

@staff_member_required
def teacher_home(request):
    assignments=Assignment.objects.all()
    return render(request,'teacher_home.html',{'assignments':assignments})

@staff_member_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request,'Assignment Created')
            return redirect('teacher_home')
    else:
        form = AssignmentForm()
    return render(request, 'create_assignment.html', {'form': form})

@staff_member_required
def delete_assignment(request,id):
    context ={} 
    obj = get_object_or_404(Assignment, id = id) 
    if request.method =="POST": 
        obj.delete() 
        messages.success(request,'Assignment deleted')
        return redirect('teacher_home')  
    return render(request,'delete_assignment.html',context)


@staff_member_required
def report_assignment(request,id):
    obj=get_object_or_404(Assignment,id=id)
    report=f'files/{obj.subject}/{obj.name}/report.txt'
    flag=False
    mean=None
    median=None
    minimum=None
    maximum=None
    total=None
    range=None
    students={}
    if path.exists(report):
        if os.stat(report).st_size>0:
            flag=True
            fh=open(report)
            contents = fh.read()
            contents = contents.splitlines()
            for line in contents:
                if line.startswith("mean"):
                    mean=float(line[line.index("=")+1:])
                elif line.startswith("median"):
                    median=float(line[line.index("=")+1:])
                elif line.startswith("minimum"):
                    minimum=float(line[line.index("=")+1:])
                elif line.startswith("maximum"):
                    maximum=float(line[line.index("=")+1:])
                elif line.startswith("total"):
                    total=float(line[line.index("=")+1:])
                else:
                    A=line
                    A=A.replace(f"files/{obj.subject}/{obj.name}/","")
                    key=A[:A.index("=")]
                    value=float(line[line.index("=")+1:])
                    students[key]=value
    if flag:
        range=maximum-minimum
    context={"flag":flag,"students":students,"mean":mean,"median":median,"minimum":minimum,"maximum":maximum,"total":total,"range":range}
    return render(request,'report_assignment.html',context)
    # return render(request,'report_submission.html')

def teacher_logout(request):
    logout(request)
    return redirect('core_home')