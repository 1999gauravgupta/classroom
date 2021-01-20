from django.db.models.signals import post_save
from .models import Submission
from django.dispatch import receiver
import subprocess
import threading
from threading import Thread

def spawner(subject,name,language,max_marks):
    path=f"files/{subject}/{name}/"
    with open(f"{path}report.txt", "w") as fp: 
        subprocess.run(f"python reporter.py --language={language} --path={path} --marks={max_marks}",shell=True,stdout=fp)

@receiver(post_save,sender=Submission)
def schedule_report_generation(sender,instance,**kwargs):
    subject=instance.assignment.subject
    name=instance.assignment.name
    language=instance.assignment.language
    max_marks=instance.assignment.max_marks
    t=Thread(target=spawner,args=(subject,name,language,max_marks))
    t.deamon=True
    t.start()