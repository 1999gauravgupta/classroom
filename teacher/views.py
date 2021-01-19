from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from .models import Assignment
from .forms import AssignmentForm
from django.contrib import messages

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
    return render(request,'report_assignment.html')

def teacher_logout(request):
    logout(request)
    return redirect('core_home')