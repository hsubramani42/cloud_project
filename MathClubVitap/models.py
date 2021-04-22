from django.db import models
class Member(models.Model):
    username=models.CharField(max_length=40,primary_key=True)
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=15)
    regno=models.CharField(max_length=10)
    type=models.CharField(max_length=2)
    tackle=models.CharField(max_length=1)
class Admin(models.Model):
    username = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=15)
class TempMember(models.Model):
    username=models.CharField(max_length=40,primary_key=True)
    name=models.CharField(max_length=30)
    regno=models.CharField(max_length=10)
    password=models.CharField(max_length=15)
class TackleMember(models.Model):
    file=models.FileField(upload_to="tackle/%Y/%m/%d/",blank=True,null=True)
    member=models.ForeignKey(Member,on_delete=models.CASCADE,blank=True,null=True)
class Feedback(models.Model):
    member=models.ForeignKey(Member,on_delete=models.CASCADE,blank=True,null=True)
    type=models.CharField(max_length=10)
    text=models.CharField(max_length=200)
    id=models.CharField(max_length=4,primary_key=True)
class FileCSV(models.Model):
    name=models.CharField(max_length=8)
    file=models.FileField(upload_to="data/")
class Topscores(models.Model):
    member=models.ForeignKey(Member,on_delete=models.CASCADE,blank=True,null=True)
    score=models.CharField(max_length=4)
class Message(models.Model):
    name=models.CharField(max_length=40,primary_key=True)
    message=models.CharField(max_length=300)
class EventCreator(models.Model):
    eventName=models.CharField(max_length=20,primary_key=True);
    description=models.CharField(max_length=300)
    team=models.CharField(max_length=1)
class EventMember(models.Model):
    username = models.CharField(max_length=40,blank=False,null=False)
    regno = models.CharField(max_length=10,blank=False,null=False)
    slot=models.CharField(max_length=8)
    teamID=models.CharField(max_length=5)
    eventName=models.CharField(max_length=20)