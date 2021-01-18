from django.db import models

# Create your models here.
class Assignment(models.Model):
    subject=models.CharField(max_length=120)
    name=models.CharField(max_length=120)
    max_marks=models.IntegerField()

    def __str__(self):
        return f'{self.subject}-{self.name}'