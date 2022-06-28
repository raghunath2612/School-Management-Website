from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sqlserverconnect.decorators import allowed_users

import pyodbc
@login_required(login_url='/')
@allowed_users(allowed_roles=["admin"])
def searchcategory(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=LAPTOP-8J652NOT\MSSQLSERVER01;'
                          'Database=Students;'
                          'Trusted_Conntection=yes;')
    cursor = conn.cursor()
    stusearchobj =[]
    if request.method=="POST":
        appno=request.POST.get('appno')
        name=request.POST.get('name')
        if not name and appno: 
            cursor.execute("select * from student s INNER JOIN familydetails f on s.appno = f.appno where s.appno like '%"+appno+"%'")
            stusearchobj = cursor.fetchall()
            return render(request,'search.html',{"studentData":stusearchobj})
        elif not appno and name :
            cursor.execute("select * from student s INNER JOIN familydetails f on s.appno = f.appno where s.firstname like '%"+name+"%' or s.middlename like '%"+name+"%' or s.lastname like '%"+name+"%' or f.fathername like '%"+name+"%' or f.mothername like '%"+name+"%'")
            stusearchobj = cursor.fetchall()
            return render(request,'search.html',{"studentData":stusearchobj})
        else:
            cursor.execute("select * from student s INNER JOIN familydetails f on s.appno = f.appno where s.appno like '%"+appno+"%' and s.firstname like '%"+name+"%' or s.middlename like '%"+name+"%' or s.lastname like '%"+name+"%' or f.fathername like '%"+name+"%' or f.mothername like '%"+name+"%'")
            stusearchobj = cursor.fetchall()
            return render(request,'search.html',{"studentData":stusearchobj})   
    else:
        return render(request,'search.html',{"studentData":[]})



@login_required(login_url='/')
@allowed_users(allowed_roles=["admin"])
def classcategory(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=LAPTOP-8J652NOT\MSSQLSERVER01;'
                          'Database=Students;'
                          'Trusted_Conntection=yes;')
    cursor = conn.cursor()
    classobj =[]
    if request.method=="POST":
        presentclass=request.POST.get('presentclass')
        section=request.POST.get('section')

        if not section and presentclass!="Select Class": 
            print("select * from student s INNER JOIN familydetails f on s.appno = f.appno where s.presentclass = '"+presentclass+"'")
            cursor.execute("select * from student s INNER JOIN familydetails f on s.appno = f.appno where s.presentclass = '"+presentclass+"'")
            classobj = cursor.fetchall()
            return render(request,'searchClassDetails.html',{"classData":classobj})

        elif presentclass=="Select Class" and section:
            print("select * from student s INNER JOIN familydetails f on s.appno = f.appno where s.section = '"+section+"'")
            cursor.execute("select * from student s INNER JOIN familydetails f on s.appno = f.appno where s.section = '"+section+"'")
            classobj = cursor.fetchall()
            return render(request,'searchClassDetails.html',{"classData":classobj})
        else:
            print("select * from student s INNER JOIN familydetails f on s.appno = f.appno where s.presentclass = '"+presentclass+"' and s.section = '"+section+"'")
            cursor.execute("select * from student s INNER JOIN familydetails f on s.appno = f.appno where s.presentclass = '"+presentclass+"' and s.section = '"+section+"'")
            # print("select appno,firstname,middlename,lastname,gender,presentclass,section from student where presentclass = "+presentclass+" and section = "+section+" ")
            classobj = cursor.fetchall()
            return render(request,'searchClassDetails.html',{"classData":classobj})   
    else:
        return render(request,'searchClassDetails.html',{"classData":[]})