from django.db.models.query_utils import PathInfo
from django.contrib.auth.decorators import login_required
from sqlserverconnect.models import Certificates
from sqlserverconnect.models import insertData
from django.http import HttpResponseRedirect
from datetime import datetime,date
import pyodbc
import os
from sqlserverconnect.forms import UserLoginForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User,Group
from sqlserverconnect.decorators import create_student_account,allowed_users


from django.contrib.auth import (
    authenticate,
    login,
    logout
)


# Create your views here.


class UserLoginView(View):
    """
    Description:Will be used to login and logout users.\n
    """
    template_name = 'login.html'
    def get(self,request,*args,**kwargs):
        form = UserLoginForm()
        context = {
            "title":"Login",
            "form":form
        }
        return render(request,self.template_name,context)

    

    def post(self,request,*args,**kwargs):
        print(request.POST)
        form = UserLoginForm(data = request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(username, password)
            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect("home/")
            
            else:
                return redirect("login/")
        else: print(form.errors)
        context = {
            "title":"Login",
            "form":form
        }
        return render(request,self.template_name,context)


def logout_view(request):
    logout(request)
    return redirect('/')



#Home page
@login_required(login_url='/')
@allowed_users(allowed_roles=["admin"])
def home(request):
    print('entered to check registration')
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=LAPTOP-8J652NOT\MSSQLSERVER01;'
                          'Database=Students;'
                          'Trusted_Conntection=yes;')
    cursor = conn.cursor()
    if request.method=="POST":
        #Getting all the student appno's
        cursor.execute('select appno from student')
        appnos = cursor.fetchall()

        #Taking appno from user
        appno=request.POST.get('appno')

        #Flag Value to check whether the given appno is there or not in student db
        flag=False

        for i in appnos:
            #comparing db appno and input appno
            #If appno is already there then check how many forms are filled
            if(i.appno==int(appno)):
                print("Appno is present")
                #Making sure that the appno is already present in student db
                flag=True
        
        #If appno is not present create a new student with appno
        if flag==False:
            #For first page
            today=date.today()
            cursor.execute("insert into student values(NULL,NULL,NULL,"+appno+",NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,'"+str(today)+"',NULL,NULL)")
            cursor.execute('insert into address values('+appno+',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)')
            cursor.execute('insert into healthdetails values('+appno+',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)')

            #For second page
            cursor.execute("insert into specialtalents values("+appno+",'','','','','','')")
            cursor.execute('insert into mediumofinstruction values('+appno+',NULL,NULL,NULL)')
            cursor.execute("insert into emergencycontactdetails values("+appno+",'',NULL)")

            #For third page
            cursor.execute("insert into familydetails values("+appno+",'','','','','','','','','','',NULL,NULL,'','',NULL,NULL,'','',NULL,NULL,NULL,NULL,NULL,NULL)")
            cursor.execute('insert into schoolsource values('+appno+',NULL,NULL,NULL)')
            
            #For fourth page
            cursor.execute("insert into certificates values("+appno+",'','','','','','','','','','','','','','')")
            cursor.commit()

        #At last opening updation page for student
        return HttpResponseRedirect('/register/'+appno+'/1')
    else:
        return render(request,'registration/register.html')



@login_required(login_url='/')
@allowed_users(allowed_roles=["admin"])
def register(request,appno,pageno):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=LAPTOP-8J652NOT\MSSQLSERVER01;'
                          'Database=Students;'
                          'Trusted_Conntection=yes;')
    #converting appno to string
    appno=str(appno)
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

                return render(request, 'registration/register1.html', {'entry': result[0],'temp':dic,'castedic':castedic,'healthdetails':healthdetails[0],'healthdic':healthdic,'address':address[0],'classdic':classdic})
            except:
                return render(request, 'registration/register1.html',{'castedic':castedic})
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


                return render(request, 'registration/register2.html',{'specialtalents':speicaltalents[0],'emergencycontactdetails':emergencycontactdetails[0],'mlanguagedic':mlanguagedic,'previousschoollis':previousschoollis,'rowlimit':rowlimit})
            except:
                return render(request,'registration/register2.html')
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

                return render(request, 'registration/register3.html', {'familydetails':familydetails[0],'transferablejob':transferablejob,'schoolsourcedic':schoolsourcedic,'siblingslis':siblingslis,'rowlimit':rowlimit})
            except:
                return render(request, 'registration/register3.html')
        elif pageno==4:
            print("Entered to page 4 get")
            cursor = conn.cursor()
            cursor.execute('select * from certificates where appno='+appno)
            certificates =cursor.fetchall()
            
            pathdic={}
            pathdic['dob']=certificates[0][1]
            pathdic['transfer']=certificates[0][2]
            pathdic['previous']=certificates[0][3]
            pathdic['aadhar']=certificates[0][4]
            pathdic['aadhar_f']=certificates[0][5]
            pathdic['blood']=certificates[0][6]
            pathdic['caste']=certificates[0][7]
            pathdic['handicap']=certificates[0][8]
            pathdic['resident']=certificates[0][9]
            pathdic['guardian']=certificates[0][10]
            pathdic['other1']=certificates[0][11]
            pathdic['other2']=certificates[0][12]
            pathdic['passphoto']=certificates[0][13]

            required_dic={}
            required_dic['dob']="" if certificates[0][1]!=""  else "required"
            required_dic['transfer']="" if certificates[0][2]!=""  else "required"
            required_dic['previous']="" if certificates[0][3]!=""  else "required"
            required_dic['aadhar']="" if certificates[0][4]!=""  else "required"
            required_dic['aadhar_f']="" if certificates[0][5]!=""  else "required"
            required_dic['blood']="" if certificates[0][6]!=""  else "required"
            required_dic['caste']="" if certificates[0][7]!=""  else "required"
            required_dic['handicap']="" if certificates[0][8]!=""  else "required"
            required_dic['resident']="" if certificates[0][9]!=""  else "required"
            required_dic['guardian']="" if certificates[0][10]!=""  else "required"
            required_dic['passphoto']="" if certificates[0][13]!=""  else "required"
            return render(request, 'registration/register4.html',{'pathdic':pathdic,'requireddic':required_dic})
   
    if request.method == "POST":

        if pageno==1:
            print("Entered to post 1st page")
            if request.POST.get('firstname') and request.POST.get('lastname') and request.POST.get('aadharno') and request.POST.get('dob') and request.POST.get('gender') and request.POST.get('pob') and request.POST.get('caste') and request.POST.get('pmobno') and request.POST.get('mtongue') and request.POST.get('idmark1') and request.POST.get('smsmobno'):
                print('entered to save records')
                
                if request.POST.get('bldgrp') and request.POST.get('lefteyesight') and request.POST.get('righteyesight') and request.POST.get('disability') and request.POST.get('doctorname') and request.POST.get('doctorno') and request.POST.get('allergies') and request.POST.get('difficulties'):
                    print('entered to health details')
                    if request.POST.get('hno') and request.POST.get('area') and request.POST.get('landmark') and request.POST.get('town') and request.POST.get('pincode'):
                        print('entered to address')
                        insertsvalues = insertData()
                        insertsvalues.firstname = request.POST.get('firstname')
                        insertsvalues.middlename = request.POST.get('middlename')
                        insertsvalues.lastname = request.POST.get('lastname')
                        #Assigning appno from url parameters
                        insertsvalues.appno = appno
                        insertsvalues.aadharno = request.POST.get('aadharno')
                        insertsvalues.dob = request.POST.get('dob')
                        insertsvalues.gender = request.POST.get('gender')
                        insertsvalues.pob = request.POST.get('pob')
                        insertsvalues.caste = request.POST.get('caste')
                        insertsvalues.subcaste=request.POST.get('subcaste')
                        insertsvalues.pmobno = request.POST.get('pmobno')
                        insertsvalues.mtongue = request.POST.get('mtongue')
                        insertsvalues.idmark1 = request.POST.get('idmark1')
                        insertsvalues.idmark2 = request.POST.get('idmark2')
                        insertsvalues.smsmobno = request.POST.get('smsmobno')
                        insertsvalues.presentclass=request.POST.get('presentclass')
                        insertsvalues.isactive=request.POST.get('isactive')
                        insertsvalues.section=request.POST.get('section')
                        print('present class',insertsvalues.presentclass)
                        
                        #Address
                        insertsvalues.hno = request.POST.get('hno')
                        insertsvalues.area = request.POST.get('area')
                        insertsvalues.landmark = request.POST.get('landmark')
                        insertsvalues.town = request.POST.get('town')
                        insertsvalues.pincode = request.POST.get('pincode')

                        #Health details
                        insertsvalues.bldgrp = request.POST.get('bldgrp')
                        insertsvalues.lefteyesight = request.POST.get(
                            'lefteyesight')
                        insertsvalues.righteyesight = request.POST.get(
                            'righteyesight')
                        insertsvalues.disability = request.POST.get('disability')
                        insertsvalues.doctorname = request.POST.get('doctorname')
                        insertsvalues.doctorno = request.POST.get('doctorno')
                        insertsvalues.allergies = request.POST.get('allergies')
                        insertsvalues.difficulties = request.POST.get(
                            'difficulties')

                        '''#Special Talents
                            insertsvalues.childtalent = request.POST.get('childtalent')
                            insertsvalues.fathertalent = request.POST.get('fathertalent')
                            insertsvalues.mothertalent = request.POST.get('mothertalent')'''

                        cursor = conn.cursor()
                        #Updating personal details
                        cursor.execute("update student set firstname='"+insertsvalues.firstname+"',middlename='"+insertsvalues.middlename+"',lastname='"+insertsvalues.lastname+"',aadharno="+insertsvalues.aadharno+",dob=convert(date,'" + insertsvalues.dob+"',102),gender='"+insertsvalues.gender+"',pob='"+insertsvalues.pob+"',caste='"+insertsvalues.caste+"',pmobno="+insertsvalues.pmobno+",mtongue='"+insertsvalues.mtongue+"',idmark1='"+insertsvalues.idmark1+"',idmark2='"+insertsvalues.idmark2+"',smsmobno="+insertsvalues.smsmobno+",subcaste='"+insertsvalues.subcaste+"',presentclass='"+insertsvalues.presentclass+"',isactive='"+insertsvalues.isactive+"',section='"+insertsvalues.section+"' where appno="+insertsvalues.appno)

                        #Updating address
                        cursor.execute("update address set hno='"+insertsvalues.hno+"',area='"+insertsvalues.area+"',landmark='"+insertsvalues.landmark+"',town='"+insertsvalues.town+"',pincode="+insertsvalues.pincode+" where appno="+insertsvalues.appno)

                        #Updating health details
                        cursor.execute("update healthdetails set bldgrp='"+insertsvalues.bldgrp+"',lefteyesight='"+insertsvalues.lefteyesight+"',righteyesight='"+insertsvalues.righteyesight+"',disability='"+insertsvalues.disability+"',doctorname='"+insertsvalues.doctorname+"',doctorno="+insertsvalues.doctorno+",allergies='"+insertsvalues.allergies+"',difficulties='"+insertsvalues.difficulties+"' where appno="+insertsvalues.appno)

                        cursor.commit()
                        print("save records completed")
                        return HttpResponseRedirect('2')
                else:
                    print('health details error')
            else:
                print("personal details error")
        
        elif pageno==2:
            print('entered to post 2nd page')

            cursor = conn.cursor()


            insertsvalues=insertData()

            #Special Talents
            insertsvalues.appno=appno
            insertsvalues.childtalent1=request.POST.get('childtalent1')
            insertsvalues.childtalent2=request.POST.get('childtalent2')
            insertsvalues.mothertalent1=request.POST.get('mothertalent1')
            insertsvalues.mothertalent2=request.POST.get('mothertalent2')
            insertsvalues.fathertalent1=request.POST.get('fathertalent1')
            insertsvalues.fathertalent2=request.POST.get('fathertalent2')

            #Medium of instruction
            insertsvalues.mlanguage1=request.POST.get('mlanguage1')
            insertsvalues.mlanguage2=request.POST.get('mlanguage2')
            insertsvalues.mlanguage3=request.POST.get('mlanguage3')

            #Emergency Contact Details
            insertsvalues.ecname=request.POST.get('ecname')
            insertsvalues.ecmob=request.POST.get('ecmob')


            #Previous school1
            insertsvalues.pschool1=request.POST.get('school1cb')
            insertsvalues.pschool2=request.POST.get('school2cb')
            

            #Previous school
            cursor.execute("delete from previousschool where appno="+appno)
            rowlimit=int(request.POST.get("rowlimit"))
            count=0
            lis=[]
            for i in range(1,rowlimit+1):
                temp=[]
                for j in range(1,7+1):
                    count+=1
                    temp.append([count,request.POST.get(str(count))])
                lis.append(temp)

            for i in lis:
                #print(i[0][0],i[0][1],i[1][0],i[1][1],i[2][0],i[2][1])
                cursor.execute("insert into previousschool values("+str(appno)+","+str(i[0][0])+",'"+i[0][1]+"',"+str(i[1][0])+",'"+i[1][1]+"',"+str(i[2][0])+",'"+i[2][1]+"',"+str(i[3][0])+",'"+i[3][1]+"',"+str(i[4][0])+",'"+i[4][1]+"',"+str(i[5][0])+",'"+i[5][1]+"',"+str(i[6][0])+",'"+i[6][1]+"')")
            


            #Speical Talents
            cursor.execute("update specialtalents set childtalent1='"+insertsvalues.childtalent1+"',childtalent2='"+insertsvalues.childtalent2+"',fathertalent1='"+insertsvalues.fathertalent1+"',fathertalent2='"+insertsvalues.fathertalent2+"',mothertalent1='"+insertsvalues.mothertalent1+"',mothertalent2='"+insertsvalues.mothertalent2+"' where appno="+insertsvalues.appno)

            #Medium of instruction
            cursor.execute("update mediumofinstruction set mlanguage1='"+insertsvalues.mlanguage1+"',mlanguage2='"+insertsvalues.mlanguage2+"',mlanguage3='"+insertsvalues.mlanguage3+"' where appno="+insertsvalues.appno)

            #Emergency Contact Details
            cursor.execute("update emergencycontactdetails set ecname='"+insertsvalues.ecname+"',ecmob="+insertsvalues.ecmob+" where appno="+insertsvalues.appno)
            cursor.commit()
            return HttpResponseRedirect('3')
        
        elif pageno==3:
            print('entered to post 3rd page')

            cursor = conn.cursor()

            insertsvalues=insertData()

            #Family Details
            insertsvalues.appno=appno
            insertsvalues.fathername=request.POST.get('fathername')
            insertsvalues.mothername=request.POST.get('mothername')
            insertsvalues.fathernationality=request.POST.get('fathernationality')
            insertsvalues.mothernationality=request.POST.get('mothernationality')
            insertsvalues.fatherqualification=request.POST.get('fatherqualification')
            insertsvalues.motherqualification=request.POST.get('motherqualification')
            insertsvalues.fatherprofession=request.POST.get('fatherprofession')
            insertsvalues.motherprofession=request.POST.get('motherprofession')
            insertsvalues.fatherofficeaddress=request.POST.get('fatherofficeaddress')
            insertsvalues.motherofficeaddress=request.POST.get('motherofficeaddress')
            insertsvalues.fatherannualincome=request.POST.get('fatherannualincome')
            insertsvalues.motherannualincome=request.POST.get('motherannualincome')
            insertsvalues.fathertransferablejob=request.POST.get('fathertransferablejob')
            insertsvalues.mothertransferablejob=request.POST.get('mothertransferablejob')
            insertsvalues.fatheradhaarno=request.POST.get('fatheradhaarno')
            insertsvalues.motheradhaarno=request.POST.get('motheradhaarno')
            insertsvalues.fatheremail=request.POST.get('fatheremail')
            insertsvalues.motheremail=request.POST.get('motheremail')
            insertsvalues.fatherteleno=request.POST.get('fatherteleno')
            insertsvalues.motherteleno=request.POST.get('motherteleno')
            insertsvalues.fatherofficeno=request.POST.get('fatherofficeno')
            insertsvalues.motherofficeno=request.POST.get('motherofficeno')
            insertsvalues.fathersms=request.POST.get('fathersms')
            insertsvalues.mothersms=request.POST.get('mothersms')

            #School Source 
            insertsvalues.newspaper=request.POST.get('newspaper')
            insertsvalues.friends=request.POST.get('friends')
            insertsvalues.web=request.POST.get('web')


            #Siblings
            cursor.execute("delete from siblings where appno="+appno)
            rowlimit=int(request.POST.get("rowlimit"))
            count=0
            lis=[]
            for i in range(1,rowlimit+1):
                temp=[]
                for j in range(1,3+1):
                    count+=1
                    temp.append([count,request.POST.get(str(count))])
                lis.append(temp)
            

            for i in lis:
                #print(i[0][0],i[0][1],i[1][0],i[1][1],i[2][0],i[2][1])
                cursor.execute("insert into siblings values("+str(appno)+","+str(i[0][0])+",'"+i[0][1]+"',"+str(i[1][0])+",'"+i[1][1]+"',"+str(i[2][0])+",'"+i[2][1]+"')")

            #Family details
            
            cursor.execute("update familydetails set fathername='"+insertsvalues.fathername+"',mothername='"+insertsvalues.mothername+"',fathernationality='"+insertsvalues.fathernationality+"',mothernationality='"+insertsvalues.mothernationality+"',fatherqualification='"+insertsvalues.fatherqualification+"',motherqualification='"+insertsvalues.motherqualification+"',fatherprofession='"+insertsvalues.fatherprofession+"',motherprofession='"+insertsvalues.motherprofession+"',fatherofficeaddress='"+insertsvalues.fatherofficeaddress+"', motherofficeaddress='"+insertsvalues. motherofficeaddress+"',fatherannualincome="+insertsvalues.fatherannualincome+",motherannualincome="+insertsvalues.motherannualincome+",fathertransferablejob='"+insertsvalues.fathertransferablejob+"',mothertransferablejob='"+insertsvalues.mothertransferablejob+"',fatheradhaarno="+insertsvalues.fatheradhaarno+",motheradhaarno="+insertsvalues.motheradhaarno+",fatheremail='"+insertsvalues.fatheremail+"',motheremail='"+insertsvalues.motheremail+"',fatherteleno="+insertsvalues.fatherteleno+",fathersms="+insertsvalues.fathersms+" where appno="+insertsvalues.appno)
            
            #For number fields that can be NULL values
            if(insertsvalues.motherteleno):
                cursor.execute("update familydetails set motherteleno="+insertsvalues.motherteleno+" where appno="+insertsvalues.appno)
            else:
                cursor.execute("update familydetails set motherteleno=NULL where appno="+insertsvalues.appno)

            if(insertsvalues.fatherofficeno):
                cursor.execute("update familydetails set fatherofficeno="+insertsvalues.fatherofficeno+" where appno="+insertsvalues.appno)
            else:
                cursor.execute("update familydetails set fatherofficeno=NULL where appno="+insertsvalues.appno)

            if(insertsvalues.motherofficeno):
                cursor.execute("update familydetails set motherofficeno="+insertsvalues.motherofficeno+" where appno="+insertsvalues.appno)
            else:
                cursor.execute("update familydetails set motherofficeno=NULL where appno="+insertsvalues.appno)

            if(insertsvalues.mothersms):
                cursor.execute("update familydetails set mothersms="+insertsvalues.mothersms+" where appno="+insertsvalues.appno)
            else:
                cursor.execute("update familydetails set mothersms=NULL where appno="+insertsvalues.appno)


            #School Source
            if insertsvalues.newspaper:
                cursor.execute("update schoolsource set newspaper='"+insertsvalues.newspaper+"' where appno="+insertsvalues.appno)
            else:
                cursor.execute("update schoolsource set newspaper=NULL where appno="+insertsvalues.appno)
            
            if insertsvalues.friends:
                cursor.execute("update schoolsource set friends='"+insertsvalues.friends+"' where appno="+insertsvalues.appno)
            else:
                cursor.execute("update schoolsource set friends=NULL where appno="+insertsvalues.appno)

            if insertsvalues.web:
                cursor.execute("update schoolsource set web='"+insertsvalues.web+"' where appno="+insertsvalues.appno)
            else:
                cursor.execute("update schoolsource set web=NULL where appno="+insertsvalues.appno)
            
            cursor.commit()
            return HttpResponseRedirect('4')

        elif pageno==4:
            print('Entered to post 4 page')
            cursor = conn.cursor()
            pathdic={}
            cert=Certificates()
            path=""
            previouspath=""
            #Retrieving files from html form
            try:
                cert.dob=request.FILES["certificate_dob"]
                dobinstance=Certificates(dob=cert.dob)
                dobinstance.id=appno
                dobinstance.save()
                path="/media/"+dobinstance.dob.name
                #For removing old file from files
                cursor.execute("select dob from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))

                cursor.execute("update certificates set dob='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass

            try:
                cert.transfer=request.FILES["certificate_transfer"]
                transferinstance=Certificates(transfer=cert.transfer)
                transferinstance.id=appno
                transferinstance.save()
                path="/media/"+transferinstance.transfer.name

                #For removing old file from files
                cursor.execute("select transfer from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                cursor.execute("update certificates set transfer='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass

            try:
                cert.previous=request.FILES["certificate_previous"]
                previousinstance=Certificates(previous=cert.previous)
                previousinstance.id=appno
                previousinstance.save()
                path="/media/"+previousinstance.previous.name

                #For removing old file from files
                cursor.execute("select previous from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                cursor.execute("update certificates set previous='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass
                
            try:
                cert.aadhar=request.FILES["certificate_aadhar"]
                aadharinstance=Certificates(aadhar=cert.aadhar)
                aadharinstance.id=appno
                aadharinstance.save()
                path="/media/"+aadharinstance.aadhar.name

                cursor.execute("select aadhar from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                cursor.execute("update certificates set aadhar='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass

            
            try:
                cert.aadhar_f=request.FILES["certificate_aadhar_f"]
                aadhar_finstance=Certificates(aadhar_f=cert.aadhar_f)
                aadhar_finstance.id=appno
                aadhar_finstance.save()
                path="/media/"+aadhar_finstance.aadhar_f.name

                cursor.execute("select aadhar_f from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                cursor.execute("update certificates set aadhar_f='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass

            try:
                cert.blood=request.FILES["certificate_blood"]
                bloodinstance=Certificates(blood=cert.blood)
                bloodinstance.id=appno
                bloodinstance.save()
                path="/media/"+bloodinstance.blood.name

                cursor.execute("select blood from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                cursor.execute("update certificates set blood='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass

            try:
                cert.caste=request.FILES["certificate_caste"]
                casteinstance=Certificates(caste=cert.caste)
                casteinstance.id=appno
                casteinstance.save()
                path="/media/"+casteinstance.caste.name
                
                cursor.execute("select caste from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                cursor.execute("update certificates set caste='"+path+"' where appno="+appno)
                os.remove(previouspath)     
            except:
                pass


            try:
                cert.handicap=request.FILES["certificate_handicap"]
                handicapinstance=Certificates(handicap=cert.handicap)
                handicapinstance.id=appno
                handicapinstance.save()

                cursor.execute("select handicap from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                path="/media/"+handicapinstance.handicap.name
                cursor.execute("update certificates set handicap='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass

            try:
                cert.resident=request.FILES["certificate_resident"]
                residentinstance=Certificates(resident=cert.resident)
                residentinstance.id=appno
                residentinstance.save()

                cursor.execute("select resident from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                path="/media/"+residentinstance.resident.name
                cursor.execute("update certificates set resident='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass

            try:
                cert.guardian=request.FILES["certificate_guardian"]
                guardianinstance=Certificates(guardian=cert.guardian)
                guardianinstance.id=appno
                guardianinstance.save()

                cursor.execute("select guardian from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                path="/media/"+guardianinstance.guardian.name
                cursor.execute("update certificates set guardian='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass
            
            try:
                cert.other1=request.FILES["certificate_other"]
                other1instance=Certificates(other1=cert.other1)
                other1instance.id=appno
                other1instance.save()
                path="/media/"+other1instance.other1.name

                cursor.execute("select other1 from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                cursor.execute("update certificates set other1='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass

            try:
                cert.other2=request.FILES["certificate_other2"]
                other2instance=Certificates(other2=cert.other2)
                other2instance.id=appno
                other2instance.save()
                path="/media/"+other2instance.other2.name

                cursor.execute("select other2 from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                cursor.execute("update certificates set other2='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass

            try:
                cert.passphoto=request.FILES["certificate_passphoto"]
                passphotoinstance=Certificates(passphoto=cert.passphoto)
                passphotoinstance.id=appno
                passphotoinstance.save()
                path="/media/"+passphotoinstance.passphoto.name

                cursor.execute("select passphoto from certificates where appno="+appno)
                previouspath=cursor.fetchall()
                previouspath=previouspath[0][0]
                previouspath=os.getcwd()+previouspath
                previouspath = '/'.join(previouspath.split('\\'))
                cursor.execute("update certificates set passphoto='"+path+"' where appno="+appno)
                os.remove(previouspath)
            except:
                pass
            
            #Creates a new user account
            create_student_account(appno)
            cursor.commit()
            return HttpResponseRedirect('/viewstudent/'+appno)
        





    


