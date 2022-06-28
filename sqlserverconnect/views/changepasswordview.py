from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
import pyodbc


@login_required(login_url='/')
def change_password(request):
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
    if request.method=="GET":
        return render(request,"changepassword.html",{"sname":sname,"passphoto":student[0].temp5})

    if request.method=="POST":
        pwd=request.POST.get("oldpwd")
        if request.user.check_password(pwd):
            newpwd=request.POST.get("newpwd1")
            request.user.set_password(newpwd)
            request.user.save()
            update_session_auth_hash(request, request.user)
            print("user authenticated")
            return render(request,"changepassword.html",{"response":"Password changed Successfully!!","sname":sname,"passphoto":student[0].temp5})
        else:
            return render(request,"changepassword.html",{"response":"Password was not correct","sname":sname,"passphoto":student[0].temp5})