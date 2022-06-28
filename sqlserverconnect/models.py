from django.db import models
import os

from django.db.models.fields import IntegerField

class sqlserverconn(models.Model):
    firstname=models.CharField(max_length=100)
    middlename=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    appno=models.IntegerField()
    aadharno=models.IntegerField()
    dob=models.DateField()
    gender=models.CharField(max_length=100)
    pob=models.CharField(max_length=100)
    caste=models.IntegerField()
    pmobno=models.IntegerField()

    mtongue=models.CharField(max_length=100)
    idmark1=models.CharField(max_length=100)
    idmark2=models.CharField(max_length=100)
    smsmobno=models.IntegerField()



    #Address
    hno=models.CharField(max_length=100)
    area=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    town=models.CharField(max_length=100)
    pincode=models.IntegerField()

    #Health details
    bldgrp=models.CharField(max_length=100)
    lefteyesight=models.CharField(max_length=100)
    righteyesight=models.CharField(max_length=100)
    disability=models.CharField(max_length=100)
    doctorname=models.CharField(max_length=100)
    doctorno=models.IntegerField()
    allergies=models.CharField(max_length=100)
    difficulties=models.CharField(max_length=100)


    #Special Talents
    childtalent=models.CharField(max_length=100)
    fathertalent=models.CharField(max_length=100)
    mothertalent=models.CharField(max_length=100)



    #Family details
    fathername=models.CharField(max_length=100)
    mothername=models.CharField(max_length=100)
    fathernationality=models.CharField(max_length=100)
    mothernationality=models.CharField(max_length=100)
    fatherqualification=models.CharField(max_length=100)
    motherqualification=models.IntegerField()
    fatherprofesion=models.CharField(max_length=100)
    moterprofesion=models.CharField(max_length=100)
    fatheroffice=models.CharField(max_length=100)
    motheroffice=models.CharField(max_length=100)
    fatherannualincome=models.IntegerField()
    moterannualincome=models.IntegerField()
    fathertransferablejob=models.CharField(max_length=100)
    mothertransferablejob=models.IntegerField()
    fatheradhaar=models.IntegerField()
    motheradhaar=models.IntegerField()
    fatheremail=models.CharField(max_length=100)
    motheremail=models.IntegerField()
    fathertele=models.IntegerField()
    mothertele=models.IntegerField()
    fatherofficeno=models.IntegerField()
    motherofficeno=models.IntegerField()
    fathersms=models.IntegerField()
    mothersms=models.IntegerField()



    
    
class insertData(models.Model):
    #Personal Details
    firstname=models.CharField(max_length=100)
    middlename=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    appno=models.IntegerField(null=True)
    aadharno=models.IntegerField(null=True)
    dob=models.DateField(null=True)
    gender=models.CharField(max_length=100)
    pob=models.CharField(max_length=100)
    caste=models.CharField(max_length=10)
    subcaste=models.CharField(max_length=10)
    pmobno=models.IntegerField(null=True)

    mtongue=models.CharField(max_length=100)
    idmark1=models.CharField(max_length=100)
    idmark2=models.CharField(max_length=100)
    smsmobno=models.IntegerField(null=True)
    presentclass=models.CharField(max_length=100,null=True)
    isactive=models.CharField(max_length=100,null=True)
    section=models.CharField(max_length=100,null=True)

    #Address
    hno=models.CharField(max_length=100)
    area=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    town=models.CharField(max_length=100)
    pincode=models.IntegerField(null=True)

    #Health details
    bldgrp=models.CharField(max_length=100)
    lefteyesight=models.CharField(max_length=100)
    righteyesight=models.CharField(max_length=100)
    disability=models.CharField(max_length=100)
    doctorname=models.CharField(max_length=100)
    doctorno=models.IntegerField(null=True)
    allergies=models.CharField(max_length=100)
    difficulties=models.CharField(max_length=100)


    #Special Talents
    childtalent1=models.CharField(max_length=100)
    fathertalent1=models.CharField(max_length=100)
    mothertalent1=models.CharField(max_length=100)
    childtalent2=models.CharField(max_length=100)
    fathertalent2=models.CharField(max_length=100)
    mothertalent2=models.CharField(max_length=100)


    #Previous school

    pschool1=models.CharField(max_length=10)
    pschoolname1=models.CharField(max_length=100)
    paddress1=models.CharField(max_length=200)
    pstudy1=models.CharField(max_length=100)
    pclass1=models.CharField(max_length=100)
    pmedium1=models.CharField(max_length=100)
    pmarks1=models.CharField(max_length=100)
    pboard1=models.CharField(max_length=100)

    pschool2=models.CharField(max_length=10)
    pschoolname2=models.CharField(max_length=100)
    paddress2=models.CharField(max_length=200)
    pstudy2=models.CharField(max_length=100)
    pclass2=models.CharField(max_length=100)
    pmedium2=models.CharField(max_length=100)
    pmarks2=models.CharField(max_length=100)
    pboard2=models.CharField(max_length=100)

    pschool3=models.CharField(max_length=10)
    pschoolname3=models.CharField(max_length=100)
    paddress3=models.CharField(max_length=200)
    pstudy3=models.CharField(max_length=100)
    pclass3=models.CharField(max_length=100)
    pmedium3=models.CharField(max_length=100)
    pmarks3=models.CharField(max_length=100)
    pboard3=models.CharField(max_length=100)

    pschool4=models.CharField(max_length=10)
    pschoolname4=models.CharField(max_length=100)
    paddress4=models.CharField(max_length=200)
    pstudy4=models.CharField(max_length=100)
    pclass4=models.CharField(max_length=100)
    pmedium4=models.CharField(max_length=100)
    pmarks4=models.CharField(max_length=100)
    pboard4=models.CharField(max_length=100)


    #Medium of instruction
    mlanguage1=models.CharField(max_length=100)
    mlanguage2=models.CharField(max_length=100)
    mlanguage3=models.CharField(max_length=100)

    #Emergency Contact Details
    ecname=models.CharField(max_length=50)
    ecmob=models.IntegerField(null=True)

    #Family details
    fathername=models.CharField(max_length=50)
    mothername=models.CharField(max_length=50)
    fathernationality=models.CharField(max_length=20)
    mothernationality=models.CharField(max_length=20)
    fatherqualification=models.CharField(max_length=20)
    motherqualification=models.CharField(max_length=20)
    fatherprofession=models.CharField(max_length=50)
    motherprofession=models.CharField(max_length=50)
    fatherofficeaddress=models.CharField(max_length=100)
    motherofficeaddress=models.CharField(max_length=100)
    fatherannualincome=models.IntegerField(null=True)
    motherannualincome=models.IntegerField(null=True)
    fathertransferablejob=models.CharField(max_length=20)
    mothertransferablejob=models.CharField(max_length=20)
    fatheradhaarno=models.IntegerField(null=True)
    motheradhaarno=models.IntegerField(null=True)
    fatheremail=models.CharField(max_length=100)
    motheremail=models.CharField(max_length=100)
    fatherteleno=models.IntegerField(null=True)
    motherteleno=models.IntegerField(null=True)
    fatherofficeno=models.IntegerField(null=True)
    motherofficeno=models.IntegerField(null=True)
    fathersms=models.IntegerField(null=True)
    mothersms=models.IntegerField(null=True)

    #School Source
    newspaper=models.CharField(max_length=20)
    friends=models.CharField(max_length=20)
    web=models.CharField(max_length=20)


    #Siblings
    scb1=models.CharField(max_length=20)
    sclass1=models.CharField(max_length=20)
    sname1=models.CharField(max_length=20)
    sadmission1=models.CharField(max_length=20)
    scb2=models.CharField(max_length=20)
    sclass2=models.CharField(max_length=20)
    sname2=models.CharField(max_length=20)
    sadmission2=models.CharField(max_length=20)
    scb3=models.CharField(max_length=20)
    sclass3=models.CharField(max_length=20)
    sname3=models.CharField(max_length=20)
    sadmission3=models.CharField(max_length=20)



class Certificates(models.Model):
    def upload_path_handler(instance, filename):
        return "student_{id}/{file}".format(id=instance.id, file=filename)
    appno=models.IntegerField(null=True)
    dob = models.ImageField(default="" , upload_to = upload_path_handler)
    transfer = models.ImageField(default="" , upload_to = upload_path_handler)
    previous = models.ImageField(default="" , upload_to = upload_path_handler)
    aadhar = models.ImageField(default="" , upload_to = upload_path_handler)
    aadhar_f = models.ImageField(default="" , upload_to = upload_path_handler)
    blood = models.ImageField(default="" , upload_to = upload_path_handler)
    caste = models.ImageField(default="" , upload_to = upload_path_handler)
    handicap = models.ImageField(default="" , upload_to = upload_path_handler)
    resident = models.ImageField(default="" , upload_to = upload_path_handler)
    guardian = models.ImageField(default="" , upload_to = upload_path_handler)
    other1 = models.ImageField(default="" , upload_to = upload_path_handler)
    other2 = models.ImageField(default="" , upload_to = upload_path_handler)
    passphoto = models.ImageField(default="" , upload_to = upload_path_handler)