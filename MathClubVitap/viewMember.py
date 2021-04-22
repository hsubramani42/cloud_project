from django.shortcuts import render,redirect
from .models import *
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse,HttpResponseBadRequest,Http404
from version0001.settings import BASE_URL

import os
from datetime import datetime
from django.http import QueryDict
from django.core.files.storage import Storage
import pandas as pd
import numpy as np
def login(request):
    warnings={
    'title':'','message':''
    }
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=Member.objects.get(username=username,password=password)
        except Exception:
            user=None
            warnings["title"]="Error: "
            warnings["message"]="Invalid username or password!"
        attend=""
        if(user!=None):
            dict={'name':user.name,'username':user.username,
                  'password':user.password,'regno':user.regno,
                  'type':user.type,'tackle':user.tackle}
            request.session["dict"]=dict
            request.session.set_expiry(600)
            return redirect('home')
    return render(request,'MathClubVitap/Login.html',{'warning':warnings})
def logged(request):
    message={"general":"","club":"","individual":""}
    try:
        dict=request.session["dict"]
        if(dict["tackle"]=="F"):
            dict["tackle"]=""
        attend=""
        if(dict["type"]=="NC"):
            dict["type"]=""
        if(request.method=='POST'):
            user=Member.objects.get(username=dict["username"])
            user.tackle="T"
            user.save()
            dict["tackle"]="T"
            request.session["dict"]=dict
        try:
            message["general"]=Message.objects.filter(name="All")
            if(dict["type"]!=""):
                message["club"]=Message.objects.filter(name="Club")
            message["individual"]=Message.objects.filter(name=dict["username"])
        except:
            pass
        request.session["dict"]=dict
        return render(request,"Member/home.html",{'dict':dict,"admin":message})
    except Exception:
        return redirect("login")
def profile(request):
    success={}
    warnings={'title':'','message':''}
    dict=request.session["dict"]
    if(request.method=='POST'):
        member=Member.objects.get(username=dict["username"])
        name=request.POST["name"]
        password=request.POST["password"]
        cpassword=request.POST["cpassword"]
        regno=request.POST["regno"]
        dict["name"]=name
        dict["regno"]=regno
        if(password==cpassword):
            member.name=name
            if(password!=""):
                member.password=password
                dict["password"]=password
            member.regno=regno
            request.session["password"]=password
            member.save()
            success="profile updated successfuly"
        else:
            warnings["title"]="Error! "
            warnings["message"]="Password didn't match"
    request.session["dict"]=dict
    return render(request,'Member/profile.html',{'warning':warnings,'success':success,'dict':dict})
def id():
    id=np.random.randint(0,99999)
    check=""
    try:
        check=EventMember.objects.filter(id=id)
    except Exception:
        check=None
        while(check!=None):
            id=np.random.randint(0,99999)
            try:
                check=EventMember.objects.filter(id=id)
            except Exception:
                check=None
    return id

def memdata(dict):
    data=[]
    try:
        events=EventCreator.objects.all()
        for event in events:
            flag=True
            members=EventMember.objects.filter(username=dict["username"])
            number=''
            for member in members:
                print(member.eventName,event.eventName)
                if(member.eventName==event.eventName):
                    flag=False
                    d={
                    'eventName':event.eventName,
                    'description':event.description,
                    'name':member.username,
                    'tid':member.teamID
                    }
                    data.append(d)
            if(flag):
                d={
                'eventName':event.eventName,
                'description':event.description,
                'name':'',
                'tid':'',
                }
                if(int(event.team)!=1):
                    d['number']=[0]*(int(event.team)-1)
                else:
                    d['number']=""
                data.append(d)
    except Exception as e:
        pass
    return data
def events(request):
    tid=''
    dict=request.session["dict"]
    initial="username="+dict["username"]+"&regno="+dict["regno"]+"&eventName=None"
    if(request.method=='POST'):
        tid=str(id())
        events=EventCreator.objects.all()
        data=''
        for event in events:
            try:
                data=QueryDict(request.POST[event.eventName])
            except Exception:
                pass
        username=data.getlist("username")
        regno=data.getlist("regno")
        slot=data.get("slot")
        eventName=data.get("eventName")
        for i in range(len(username)):
            try:
                event=EventMember.objects.create(username=username[i].lower(),regno=regno[i].upper(),slot=slot,teamID=tid,eventName=eventName)
                event.save()
            except Exception:
                pass
        data=memdata(dict)
        return redirect("eventRegister")
    data=memdata(dict)
    return render(request,'Member/event.html',{'dict':dict,'data':data,'initial':initial,'size':200})
def attendance(request):
    df=pd.read_csv("media/data/attendance.csv")
    dict=request.session["dict"]
    name=dict["username"]
    data=df.T[[0,1,np.argmax([df.T.head(1).to_numpy()==name])]].iloc[1:].dropna().to_numpy()
    return render(request,'Member/attendance.html',{'data':data,'dict':dict})
def tackle(request):
    file=None
    solution=None
    try:
        ques=Member.objects.get(username="Tackle")
        files=TackleMember.objects.filter(member=ques)
        file=BASE_URL+files[len(files)-1].file.url
    except:
        pass
    try:
        sol = Member.objects.get(username="TackleSol")
        files = TackleMember.objects.filter(member=sol)
        solution = BASE_URL + files[len(files) - 1].file.url
    except:
        pass
    submission=''
    message={}
    if(request.method=='POST'):
        dict=request.session["dict"]
        username=dict["username"]
        reg=dict["regno"]
        files=request.FILES.get('file')
        filename= str(files).lower()
        if(filename==reg.lower()+".pdf"):
            try:
                member=Member.objects.get(username=username)
                mem=TackleMember.objects.get_or_create(member=member,file=files)
                message["success"]="File upload successfull!"
            except Exception:
                message["warning"]="Error in uploading!"
        else:
            message["warning"]="Rename file and try again"
    topscores=""
    try:
        topscores=Topscores.objects.all()
    except Exception as e:
        pass
    dict=request.session["dict"]
    try:
        submission=TackleMember.objects.get(username=dict["username"])
    except Exception as e:
        pass
    evaluation=""
    if(datetime.now().strftime('%A')=="Saturday"):
        evaluation="Yes"
    return render(request,'Member/tackle.html',{'file':file,'evaluation':evaluation,'message':message,'dict':dict,'topscores':topscores,'submission':submission,'solution':solution})
def fid():
    id=np.random.randint(0,9999)
    check=""
    try:
        check=Feedback.objects.filter(id=id)
    except Exception:
        check=None
        while(check!=None):
            id=np.random.randint(0,99999)
            try:
                check=Feedback.objects.filter(id=id)
            except Exception:
                check=None
    return id
def feedback(request):
    message=""
    dict=request.session["dict"]
    if(request.method=='POST'):
        id=fid()
        name=request.POST["username"]
        type=request.POST["service"]
        text=request.POST["message"]
        member=Member.objects.get(username=name)
        feed=Feedback.objects.get_or_create(member=member,type=type,text=text,id=id)
        message="Your response has been recorded!"
    try:
        return render(request,'Member/feedback.html',{'dict':dict,'message':message})
    except Exception:
        return redirect('login')
def delete(request):
    try:
        dict=request.session["dict"]
        member=Member.objects.get(username=dict["username"])
        member.delete()
        tackle=TackleMember.objects.get(username=dict["username"])
        tackle.delete()
    except Exception:
        pass
    request.session.flush()
    return redirect('register')
def logout(request):
    request.session.flush()
    return redirect('login')
def download(request, path):
    try:
        path1=os.path.join("media",os.path.join("tackle",path))
        file=open(path1,'rb')
        response = HttpResponse(file, content_type='application/pdf')
        if(path=="TackleSol.pdf"):
            response['Content-Disposition'] = 'attachment; filename="TackleSol.pdf"'
        else:
            response['Content-Disposition'] = 'attachment; filename="Tackle.pdf"'
        return response
    except Exception:
        return HttpResponseBadRequest('<h1>File Not found</h1>')
