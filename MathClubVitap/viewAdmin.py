from django.shortcuts import render,redirect
from .models import *
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse,HttpResponseBadRequest
from datetime import date
import os
from django.http import QueryDict
from django.core.files import File
import pandas as pd
import numpy as np
def administrator(request):
    warnings={
    'title':'','message':''
    }
    if(request.method=='POST'):
        id=request.POST['username']
        password=request.POST['password']
        try:
            user=Admin.objects.get(username=id,password=password)
        except Exception:
            user=None
        if(user==None):
            warnings['title']='Error! '
            warnings['message']='Invalid username or password'
        else:
            request.session["name"]='Admin'
            request.session.set_expiry(900)
            return redirect('adminDashboard')
    return render(request,'Administrator/admin.html',{'warning':warnings});
def adminLogin(request):
    messages=""
    if(request.method=="POST"):
        try:
            message=request.POST["delete"]
            message=message.split("-")
            for name in message:
                try:
                    m=Message.objects.get(name=name)
                    m.delete()
                except Exception as e:
                    pass
        except Exception:
            To=request.POST["to"]
            message=request.POST["message"]
            msg=Message.objects.get_or_create(name=To,message=message)
    messages=Message.objects.all()
    options=Member.objects.all()
    try:
        name=request.session["name"]
        return render(request,'Administrator/adminDash.html',{'messages':messages,'options':options})
    except Exception:
        return redirect('administrator')
def adminLogout(request):
    try:
        if (os.path.isfile("media/data/Members.csv")):
            os.remove("media/data/Members.csv")
        try:
            if os.path.isfile("media/data/Event.csv"):
                os.remove("media/data/Event.csv")
        except Exception:
            pass
    except Exception:
        pass
    request.session.flush()
    return redirect('administrator')
def adminApprove(request):
    try:
        name=request.session["name"]
        member=TempMember.objects.all()
        if(request.method=='POST'):
            aname=request.POST["approve"]
            rname=request.POST["reject"]
            aname=aname.split("-")
            rname=rname.split("-")
            for i in aname:
                try:
                    temp=TempMember.objects.get(username=i)
                    added=Member.objects.create(username=temp.username,name=temp.name,password=temp.password,regno=temp.regno,type="NC",tackle="F")
                    added.save()
                    temp.delete()
                except Exception:
                    pass
            for i in rname:
                try:
                    temp=TempMember.objects.get(username=i)
                    temp.delete()
                except Exception:
                    pass
        return render(request,"Administrator/approve.html",{'members':member})
    except Exception:
        return redirect('administrator')
def adminEvent(request):
    try:
        name=request.session["name"]
        if(request.method=="POST"):
            try:
                names=request.POST["delete"]
                names=names.split("-")
                for name in names:
                    try:
                        eve=EventCreator.objects.get(eventName=name)
                        mem=EventMember.objects.filter(eventName=name)
                        eve.delete()
                        mem.delete()
                    except Exception as e:
                        pass
            except Exception as e:
                try:
                    string=request.POST["top3"]
                    dict=QueryDict(string)
                    regs=dict.getlist("regno")
                    scores=dict.getlist("score")
                    Topscores.objects.all().delete()
                    for i in range(len(regs)):
                        try:
                            member=Member.objects.get(regno=regs[i].upper())
                            print(member)
                            Topscores.objects.create(member=member,score=scores[i])
                        except Exception as e:
                            pass
                except Exception:
                    name=request.POST["name"]
                    description=request.POST["description"]
                    number=request.POST["number"]
                    try:
                        eve=EventCreator.objects.get_or_create(eventName=name,description=description,team=number)
                    except Exception:
                        pass
        events=EventCreator.objects.all()
        return render(request,'Administrator/adminEvent.html',{'events':events})
    except Exception:
        return redirect('administrator')
def addData(service):
    if(service=="Restore Members"):
        array=pd.read_csv("media/data/Members.csv").to_numpy()
        print(array)
        for each in array:
            try:
                mem=Member.objects.get_or_create(username=each[0].lower(),name=each[3],password=each[1],regno=each[2].upper(),type=each[4],tackle=each[5])
            except Exception as e:
                pass
        try:
            f=FileCSV.objects.get(name="Members").file
            f.delete()
            f=FileCSV.objects.get(name="Members")
            f.delete()
        except Exception:
            pass
    else:
        array=pd.read_csv("media/data/MathClub.csv").to_numpy()
        members=Member.objects.all()
        for member in members:
            try:
                member.type="NC"
                member.save()
            except Exception:
                print(Exception)
        for each in array:
            try:
                mem=Member.objects.get(username=each[0].lower())
                mem.type="CM"
                mem.tackle="T"
                mem.save()
            except Exception:
                acc=Member.objects.create(username=each[0].lower(),name=each[3],password=each[1],regno=each[2].upper(),type=each[4],tackle=each[5])
                acc.save()
        try:
            f=FileCSV.objects.get(name="MathClub").file
            f.delete()
            f=FileCSV.objects.get(name="MathClub")
            f.delete()
        except Exception:
            pass
def generate(service,file):
    dict=''
    if(service=="Backup Members"):
        temp=[]
        members=Member.objects.all()
        for member in members:
            data=[member.username,member.name,member.password,member.regno,member.type,member.tackle]
            temp.append(data)
        temp=np.array(temp)
        dict={
        'Username':temp[:,0],
        'Password':temp[:,2],
        'Reg No':temp[:,3],
        'Name':temp[:,1],
        'Type':temp[:,4],
        'Tackle':temp[:,5]
        }
        df=pd.DataFrame(dict)
        df.to_csv(file,index=False)
    else:
        data=[]
        events=EventMember.objects.all()
        for event in events:
            temp=[event.username,event.regno,event.slot,event.teamID,event.eventName]
            data.append(temp)
        data=np.array(data)
        dict={
        'Username':data[:,0],
        'Reg No':data[:,1],
        'Slot':data[:,2],
        'Team ID':data[:,3],
        'Event Name':data[:,4]
        }
        df=pd.DataFrame(dict)
        df.to_csv(file,index=False)
def data(request):
    try:
        name=request.session["name"]
        file=''
        if(request.method=='POST'):
            try:
                service=request.POST["generate"]
                if(service=="Backup Members"):
                    file="media/data/Members.csv"
                    generate(service,file)
                    file="Members.csv"
                elif(service=="Backup Event"):
                    file="media/data/Event.csv"
                    generate(service,file)
                    file="Event.csv"
                elif(service=="Tackle Question Upload"):
                    files=request.FILES.get('file')
                    try:
                        user=Member.objects.get(username="Tackle")
                        f=TackleMember.objects.get(member=user).file
                        f.delete()
                        f=TackleMember.objects.get(member=user)
                        f.delete()
                    except Exception:
                        pass
                    f=TackleMember.objects.create(member=user,file=files)
                    f.save()
                elif(service=="Tackle Solution Upload"):
                    files=request.FILES.get('file')
                    try:
                        user = Member.objects.get(username="TackleSol")
                        f=TackleMember.objects.get(member=user).file
                        f.delete()
                        f=TackleMember.objects.get(member=user)
                        f.delete()
                    except Exception:
                        pass
                    f=TackleMember.objects.create(member=user,file=files)
                    f.save()
                else:
                    files=request.FILES.get('file')
                    if(str(files)=="Members.csv"):
                        try:
                            f=FileCSV.objects.get(name="Members").file
                            f.delete()
                            f=FileCSV.objects.get(name="Members")
                            f.delete()
                        except Exception:
                            pass
                        f=FileCSV.objects.create(name="Members",file=files)
                        f.save()
                    else:
                        try:
                            f=FileCSV.objects.get(name="MathClub").file
                            f.delete()
                            f=FileCSV.objects.get(name="MathClub")
                            f.delete()
                        except Exception:
                            pass
                        f=FileCSV.objects.create(name="MathClub",file=files)
                        f.save()
                addData(service)
            except Exception:
                pass
        return render(request,'Administrator/data.html',{'file':file})
    except Exception:
        return redirect('administrator')
def adminAttendance(request):
    text=None
    if(request.method=='POST'):
        text=request.POST["text"]
        try:
            text=text.lower()
            if(text=="delete"):
                m=Attendance.objects.filter(username='Admin')
                m.delete()
                text=""
            else:
                m=Attendance.objects.create(username='Admin',hint=text,date=str(date.today()))
                m.save()
        except Exception:
            pass
    try:
        name=request.session["name"]
        return render(request,'Administrator/attendance.html',{'size':340,'text':text})
    except Exception:
        return redirect('administrator')
def feedback(request):
    if(request.method=='POST'):
        ids=request.POST["delete"]
        ids=ids.split('-')
        for i in ids:
            try:
                feed=Feedback.objects.get(id=i)
                feed.delete()
            except Exception:
                pass
    try:
        objects=Feedback.objects.all()
        request.session["name"]
        return render(request,'Administrator/feedbackView.html',{'members':objects})
    except Exception:
        return redirect("login")
def download(request,filename):
    path=os.path.join("media",os.path.join("data",filename))
    file=open(path,'rb')
    response = HttpResponse(file,content_type='text/csv')
    if(filename=="Members.csv"):
        response['Content-Disposition'] = 'attachment; filename=Members.csv'
    else:
        response['Content-Disposition'] = 'attachment; filename=Event.csv'
    return response
