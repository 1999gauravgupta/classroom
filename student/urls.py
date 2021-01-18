from django.urls import path,include
from .views import student_home,register_student,create_submission,update_submission,delete_submission,report_submission,student_logout
from .views import SubmissionListView
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('',SubmissionListView.as_view(),name="student_home"),
    path('register',register_student,name="register_student"),
    path('submit',create_submission,name="create_submission"),
    path('submission/update/<id>',update_submission,name="update_submission"),
    path('submission/delete/<id>',delete_submission,name="delete_submission"),
    path('submission/report/<id>',report_submission,name="report_submission"),
    path('logout',student_logout),
    path('oauth/', include('social_django.urls', namespace='social')),
]
