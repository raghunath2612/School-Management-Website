from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sqlserverconnect.decorators import allowed_users
from datetime import datetime,date
import pyodbc

@login_required(login_url='/')
@allowed_users(allowed_roles=["student"])
def profile_view(request,pageno):
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
    #converting appno to string
    appno=str(request.user)
    print('save records working'+request.method )
    if request.method =="GET":
        if pageno==1:
            cursor = conn.cursor()
            cursor.execute('select * from student where appno='+appno)
            result = cursor.fetchall()
            cursor.execute('select * from healthdetails where appno='+appno)
            healthdetails = cursor.fetchall()
            cursor.execute('select * from address where appno='+appno)
            address = cursor.fetchall()
            castedic={}
            castedic["isenabled"]="disabled"
            #Converting date to required format in html
            try:
                result[0].dob=datetime.strptime(result[0].dob, "%Y-%m-%d").strftime('%Y-%m-%d')
                dic={}

                #For retrieving gender in form
                if(result[0].gender=="male"):
                    dic['male']="checked"
                else:
                    dic['female']="checked"

                #For retrieving Isactive or not in form
                if(result[0].isactive=="active"):
                    dic['active']="checked"
                else:
                    dic['inactive']="checked"

                #For retrieving caste in form
                
                if result[0].caste=="BC":
                    castedic["BC"]="checked"
                elif result[0].caste=="OC":
                    castedic["OC"]="checked"
                elif result[0].caste=="SC":
                    castedic["SC"]="checked"
                elif result[0].caste=="ST":
                    castedic["ST"]="checked"
                elif result[0].caste=="PC":
                    castedic["PC"]="checked"
                
                #For retrieving Subcaste
                
                if result[0].caste=="BC":
                    castedic["isenabled"]="enabled"
                    if result[0].subcaste=="None":
                        castedic["None"]="selected"
                    elif result[0].subcaste=="BC-A":
                        castedic["BCA"]="selected"
                    elif result[0].subcaste=="BC-B":
                        castedic["BCB"]="selected"
                    if result[0].subcaste=="BC-C":
                        castedic["BCC"]="selected"
                    elif result[0].subcaste=="BC-D":
                        castedic["BCD"]="selected"

                #For retrieving blood group
                healthdic={}
                if healthdetails[0].bldgrp=="A+":
                    healthdic["AP"]="selected"
                elif healthdetails[0].bldgrp=="A-":
                    healthdic["AN"]="selected"
                elif healthdetails[0].bldgrp=="B+":
                    healthdic["BP"]="selected"
                elif healthdetails[0].bldgrp=="B-":
                    healthdic["BN"]="selected"
                elif healthdetails[0].bldgrp=="AB+":
                    healthdic["ABP"]="selected"
                elif healthdetails[0].bldgrp=="AB-":
                    healthdic["ABN"]="selected"
                elif healthdetails[0].bldgrp=="O+":
                    healthdic["OP"]="selected"
                elif healthdetails[0].bldgrp=="O-":
                    healthdic["ON"]="selected"
                
                classdic={}
                if result[0].presentclass=="Nursery":
                    classdic["Nursery"]="selected"
                if result[0].presentclass=="LKG":
                    classdic["LKG"]="selected"
                if result[0].presentclass=="UKG":
                    classdic["UKG"]="selected"
                if result[0].presentclass=="1":
                    classdic["one"]="selected"
                if result[0].presentclass=="2":
                    classdic["two"]="selected"
                if result[0].presentclass=="3":
                    classdic["three"]="selected"
                if result[0].presentclass=="4":
                    classdic["four"]="selected"
                if result[0].presentclass=="5":
                    classdic["five"]="selected"
                if result[0].presentclass=="6":
                    classdic["six"]="selected"
                if result[0].presentclass=="7":
                    classdic["sevn"]="selected"
                if result[0].presentclass=="8":
                    classdic["eight"]="selected"
                if result[0].presentclass=="9":
                    classdic["nine"]="selected"
                if result[0].presentclass=="10":
                    classdic["ten"]="selected"

                return render(request, 'student/registration/register1.html', {'entry': result[0],'temp':dic,'castedic':castedic,'healthdetails':healthdetails[0],'healthdic':healthdic,'address':address[0],'classdic':classdic,"sname":sname,"passphoto":student[0].temp5})
            except:
                return render(request, 'student/registration/register1.html',{'castedic':castedic,"sname":sname,"passphoto":student[0].temp5})
        elif pageno==2:
            cursor = conn.cursor()
            cursor.execute('select * from specialtalents where appno='+appno)
            speicaltalents = cursor.fetchall()

            cursor.execute('select * from mediumofinstruction where appno='+appno)
            mediumofinstruction=cursor.fetchall()
            cursor.execute('select * from emergencycontactdetails where appno='+appno)
            emergencycontactdetails=cursor.fetchall()

            cursor.execute("select * from previousschool where appno="+appno)
            previousschool=cursor.fetchall()

            try:

                previousschoollis=[]
                rowlimit=len(previousschool)
                for i in previousschool:
                    print(i)
                    temp=[]
                    temp.append([i[1],i[2]])
                    temp.append([i[3],i[4]])
                    temp.append([i[5],i[6]])
                    temp.append([i[7],i[8]])
                    temp.append([i[9],i[10]])
                    temp.append([i[11],i[12]])
                    temp.append([i[13],i[14]])
                    previousschoollis.append(temp)
                #For medium of instruction
                mlanguagedic={}
                if mediumofinstruction[0].mlanguage2=="Hindi":
                    mlanguagedic['Hindi2']="checked"
                elif mediumofinstruction[0].mlanguage2=="Telugu":
                    mlanguagedic['Telugu2']="checked"
                
                if mediumofinstruction[0].mlanguage3=="Hindi":
                    mlanguagedic['Hindi3']="checked"
                elif mediumofinstruction[0].mlanguage3=="Telugu":
                    mlanguagedic['Telugu3']="checked"
                elif mediumofinstruction[0].mlanguage3=="Sanskrit":
                    mlanguagedic['Sanskrit3']="checked"


                return render(request, 'student/registration/register2.html',{'specialtalents':speicaltalents[0],'emergencycontactdetails':emergencycontactdetails[0],'mlanguagedic':mlanguagedic,'previousschoollis':previousschoollis,'rowlimit':rowlimit,"sname":sname,"passphoto":student[0].temp5})
            except:
                return render(request,'student/registration/register2.html',{"sname":sname,"passphoto":student[0].temp5})
        elif pageno==3:
            print("Entered to 3 get")
            cursor = conn.cursor()
            cursor.execute('select * from familydetails where appno='+appno)
            familydetails = cursor.fetchall()
            #print(familydetails)

            cursor.execute('select * from schoolsource where appno='+appno)
            schoolsource = cursor.fetchall()
            #print(schoolsource)

            cursor.execute("select * from siblings where appno="+appno)
            siblings=cursor.fetchall()
            
            try:
                transferablejob = {}
                schoolsourcedic = {}

                siblingslis=[]
                rowlimit=len(siblings)
                for i in siblings:
                    temp=[]
                    temp.append([i[1],i[2]])
                    temp.append([i[3],i[4]])
                    temp.append([i[5],i[6]])
                    siblingslis.append(temp)
                #print('siblings',siblingslis)
                #For retrieving transferable job yes or no in form
                if familydetails[0].fathertransferablejob=="Yes":
                    transferablejob['fatheryes']="checked"
                if familydetails[0].fathertransferablejob=="No":
                    transferablejob['fatherno']="checked"
                
                if familydetails[0].mothertransferablejob=="Yes":
                    transferablejob['motheryes']="checked"
                if familydetails[0].mothertransferablejob=="No":
                    transferablejob['motherno']="checked"

                #For retrieving school source

                if schoolsource[0].newspaper=="newspaper":
                    schoolsourcedic['newspaper']="checked"
                if schoolsource[0].friends=="friends":
                    schoolsourcedic['friends']="checked"
                if schoolsource[0].web=="web":
                    schoolsourcedic['web']="checked"

                return render(request, 'student/registration/register3.html', {'familydetails':familydetails[0],'transferablejob':transferablejob,'schoolsourcedic':schoolsourcedic,'siblingslis':siblingslis,'rowlimit':rowlimit,"sname":sname,"passphoto":student[0].temp5})
            except:
                return render(request, 'student/registration/register3.html',{"sname":sname,"passphoto":student[0].temp5})