import pyodbc
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models.query_utils import PathInfo
from django.contrib.auth.decorators import login_required
from sqlserverconnect.decorators import allowed_users

# acknowledgement


@login_required(login_url='/')
@allowed_users(allowed_roles=["admin","student"])
def view_student(request, appno):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=LAPTOP-8J652NOT\MSSQLSERVER01;'
                          'Database=Students;'
                          'Trusted_Conntection=yes;')
    try:
        cursor = conn.cursor()
        cursor.execute('select * from Student where appno='+str(appno))
        student = cursor.fetchall()
        student=student[0]
        cursor.execute('select * from address where appno='+str(appno))
        address = cursor.fetchall()
        address=address[0]
        cursor.execute('select * from healthdetails where appno='+str(appno))
        healthdetails = cursor.fetchall()
        healthdetails=healthdetails[0]
        cursor.execute('select * from specialtalents where appno='+str(appno))
        specialtalents = cursor.fetchall()
        specialtalents=specialtalents[0]
        cursor.execute('select * from previousschool where appno='+str(appno))
        previousschool = cursor.fetchall()
        cursor.execute('select * from mediumofinstruction where appno='+str(appno))
        mediumofinstruction = cursor.fetchall()
        mediumofinstruction=mediumofinstruction[0]
        cursor.execute(
            'select * from emergencycontactdetails where appno='+str(appno))
        emergencycontactdetails = cursor.fetchall()
        emergencycontactdetails=emergencycontactdetails[0]
        cursor.execute('select * from familydetails where appno='+str(appno))
        familydetails = cursor.fetchall()
        familydetails=familydetails[0]
        cursor.execute('select * from schoolsource where appno='+str(appno))
        schoolsource = cursor.fetchall()
        schoolsourcelis = []
        for i in schoolsource[0][1:]:
            if i != None:
                schoolsourcelis.append(i)
        print(schoolsourcelis)
        cursor.execute('select * from siblings where appno='+str(appno))
        siblings = cursor.fetchall()
        cursor.execute('select * from certificates where appno='+str(appno))
        certificates = cursor.fetchall()
        certificates=certificates
        dic1 = {}

        if certificates[0].passphoto == '':
            dic1['passphoto'] = "No"
        else:
            dic1['passphoto'] = "Yes"
        if certificates[0].dob == '':
            dic1['dob'] = "No"
        else:
            dic1['dob'] = "Yes"
        if certificates[0].transfer == '':
            dic1['transfer'] = "No"
        else:
            dic1['transfer'] = "Yes"
        if certificates[0].previous == '':
            dic1['previous'] = "No"
        else:
            dic1['previous'] = "Yes"
        if certificates[0].aadhar == '':
            dic1['aadhar'] = "No"
        else:
            dic1['aadhar'] = "Yes"
        if certificates[0].aadhar_f == '':
            dic1['aadhar_f'] = "No"
        else:
            dic1['aadhar_f'] = "Yes"
        if certificates[0].blood == '':
            dic1['blood'] = "No"
        else:
            dic1['blood'] = "Yes"
        if certificates[0].caste == '':
            dic1['caste'] = "No"
        else:
            dic1['caste'] = "Yes"
        if certificates[0].handicap == '':
            dic1['handicap'] = "No"
        else:
            dic1['handicap'] = "Yes"
        if certificates[0].resident == '':
            dic1['resident'] = "No"
        else:
            dic1['resident'] = "Yes"
        if certificates[0].guardian == '':
            dic1['guardian'] = "No"
        else:
            dic1['guardian'] = "Yes"
        if certificates[0].other1 == '':
            dic1['other1'] = "No"
        else:
            dic1['other1'] = "Yes"
        if certificates[0].other2 == '':
            dic1['other2'] = "No"
        else:
            dic1['other2'] = "Yes"
            
        certificates=certificates[0]
        return render(request, 'acknowledge.html', {'student': student, 'address': address, 'healthdetails': healthdetails,
                                                    'specialtalents': specialtalents, 'previousschool': previousschool, 'mediumofinstruction': mediumofinstruction,
                                                    'emergencycontactdetails': emergencycontactdetails,
                                                    'familydetails': familydetails, 'schoolsourcelis': schoolsourcelis, 'siblings': siblings, 'certificates': certificates,'dic1' : dic1})
    except:
        return render(request, "userNotRegisteredSuccessfully.html")
