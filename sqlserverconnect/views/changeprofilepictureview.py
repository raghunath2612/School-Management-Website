from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sqlserverconnect.decorators import allowed_users
from sqlserverconnect.models import Certificates
import os

import pyodbc

@login_required(login_url='/')
@allowed_users(allowed_roles=["student"])
def changePP(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=LAPTOP-8J652NOT\MSSQLSERVER01;'
                          'Database=Students;'
                          'Trusted_Conntection=yes;')
    cursor = conn.cursor()
    cursor.execute("select * from student where appno="+str(request.user))
    student=cursor.fetchall()
    sname=""
    if student[0].middlename!="":  
        sname=student[0].firstname+" "+student[0].middlename+" "+student[0].lastname
    else:
        sname=student[0].firstname+" "+student[0].lastname
    if request.method=="POST":
        cert=Certificates()
        cert.passphoto=request.FILES["certificate_passphoto"]
        passphotoinstance=Certificates(passphoto=cert.passphoto)
        appno=str(request.user)
        passphotoinstance.id=int(appno)
        passphotoinstance.save()
        path="/media/"+passphotoinstance.passphoto.name
        cursor.execute("select temp5 from student where appno="+str(request.user))
        previouspath=cursor.fetchall()
        cursor.execute("update student set temp5='"+path+"' where appno="+str(request.user))
        cursor.commit()
        try:
            
            
            previouspath=previouspath[0][0]
            previouspath=os.getcwd()+previouspath
            previouspath = '/'.join(previouspath.split('\\'))
            os.remove(previouspath)
        except:
            pass
        

        cursor.execute("select * from student where appno="+str(request.user))
        student=cursor.fetchall()
        sname=""
        if student[0].middlename!="":  
            sname=student[0].firstname+" "+student[0].middlename+" "+student[0].lastname
        else:
            sname=student[0].firstname+" "+student[0].lastname
            
        return render(request,"changeprofilepicture.html",{"response":"Profile picture changed successfully","sname":sname,"passphoto":student[0].temp5})
    else:
        return render(request,"changeprofilepicture.html",{"sname":sname,"passphoto":student[0].temp5})
