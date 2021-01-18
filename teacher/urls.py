from django.urls import path
from .views import teacher_home,create_assignment,delete_assignment,report_assignment,teacher_logout

urlpatterns = [
    path('',teacher_home,name="teacher_home"),
    path('create',create_assignment,name="create_assignment"),
    path('assignment/delete/<id>',delete_assignment,name="delete_assignment"),
    path('assignment/report/<id>',report_assignment,name="report_assignment"),
    path('logout',teacher_logout),
]
