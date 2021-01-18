from django.db import models
from teacher.models import Assignment
from django.contrib.auth.models import User
# Create your models here.

def get_username(self):
    return self.username

User.add_to_class("__str__", get_username)

def upload_location(instance, filename):
	file_path = 'files/{assignment_subject}/{assignment_name}/{student_username}-{filename}'.format(assignment_subject=str(instance.assignment.subject),assignment_name=str(instance.assignment.name),student_username=str(instance.student.username), filename=filename)
	return file_path

class Submission(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    file=models.FileField(upload_to=upload_location)

    def __str__(self):
        return f'{self.student.username}-{self.assignment.subject}-{self.assignment.name}'
