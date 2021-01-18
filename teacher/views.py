from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout

@staff_member_required
def teacher_home(request):
    return render(request,'teacher_home.html')

@staff_member_required
def create_assignment(request):
    return render(request,'create_assignment.html')

@staff_member_required
def delete_assignment(request,id):
    return render(request,'delete_assignment.html')

@staff_member_required
def report_assignment(request,id):
    return render(request,'report_assignment.html')

def teacher_logout(request):
    logout(request)
    return redirect('core_home')