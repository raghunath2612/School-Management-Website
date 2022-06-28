from django.shortcuts import render
from sqlserverconnect.decorators import allowed_users
from django.contrib.auth.decorators import login_required
import pyodbc

@login_required(login_url='/')
@allowed_users(allowed_roles=["student"])
def home(request):
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
    return render(request,"student/home.html",{"sname":sname,"passphoto":student[0].temp5})
