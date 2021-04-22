from django.shortcuts import render,redirect
from .models import Member,TempMember,Admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse,HttpResponseBadRequest
def homepage(request):
    return render(request,"MathClubVitap/index.html")
def signup(request):
    success={
    'title':'','message':''}
    warnings={
    'title':'','message':''
    }
    if(request.method=='POST'):
        name=request.POST["name"]
        email=request.POST["email"]
        email=email+"@vitap.ac.in"
        email=email.lower()
        reg=request.POST["reg"]
        reg=reg.upper()
        password=request.POST["password"]
        confirmpassword=request.POST["confirmpassword"]
        try:
            user=Member.objects.get(username=email)
        except Exception:
            user=None
        try:
            user1=TempMember.objects.get(username=email)
        except Exception:
            user1=None
        if(user==None):
            if(user1==None):
                if(password==confirmpassword):
                    user=TempMember.objects.create(username=email,password=password,name=name,regno=reg)
                    user.save()
                    success['title']="Account created successfuly! "
                    success['message']="Waiting for administrator to process your request!"
                else:
                    warnings['title']="Error: "
                    warnings['message']="Password didn't match!"
            else:
                success['title']="Thank you for your patience: "
                success['message']="Your request is under progress!"
        else:
            warnings['title']="Error: "
            warnings['message']="User already exits"
    return render(request,'MathClubVitap/Signup.html',{'success':success,'warning':warnings})
def about(request):
    return render(request,'MathClubVitap/about.html')
def events(request):
    return render(request,'MathClubVitap/event.html')
