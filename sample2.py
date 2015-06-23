import datetime
from urlparse import urlparse
from httplib import HTTPConnection
import urllib
import json
import csv

students = ['akella.keerthi@gmail.com',
            'akkineni.vidya1993@gmail.com','alluriharitha@gmail.com',
            'anveshika.09@gmail.com','ashok.kp204@gmail.com',
            'bvss.shashank@gmail.com','c.bhavana.17@gmail.com',
            'dasarianvesh100@gmail.com','deepak.m90stmfrd@gmail.com',
            'diveshreddy@gmail.com','gennycuti@gmail.com',
            'golikranthireddy@gmail.com','gopalnivedita1992@gmail.com',
            'harikavasu812@gmail.com','harikrishna8055@gmail.com',
            'harsha.ascet@gmail.com','harshadarling412@gmail.com',
            'hsharathchandra@gmail.com','jayanthsai93@gmail.com',
            'k.srirammanoj1@gmail.com','k.srirammanoj@gmail.com',
            'k.yashu13@gmail.com','karthik.pvns@gmail.com','krish.m8@gmail.com',
            'kvijay452@gmail.com','lakshman.sadineni@gmail.com',
            'lakshmiuma4002@gmail.com','madhavi.btech4@gmail.com',
            'mallela.sivaram@gmail.com','manasa.batti@gmail.com',
            'mayukh.chongdar@gmail.com','naraganisravanthi@gmail.com',
            'nareshrava@gmail.com','navyatreddy@gmail.com',
            'nikhil.psnl24@gmail.com','p.sairaghuteja@gmail.com',
            'paul.joey143@gmail.com','pavanikamireddy12@gmail.com',
	    'pmss.sameera7@gmail.com','poonamgoje@gmail.com','psk0911@gmail.com',
            'rajeev.isarapu09@gmail.com','rajtikkalaprudhvi@gmail.com',
            'reddyushasreeg28@gmail.com','rehana@msitprogram.net',
            'rgetty6@gmail.com','yasha7913@gmail.com','yroopa213@gmail.com',
	    'rockykusuma@gmail.com','rohandhaka24@gmail.com',
            'saibharadwaja92@gmail.com','saireddy192@gmail.com',
            'saiteja1111n@gmail.com','shirishdee@gmail.com',
            'siddarthrahul@gmail.com','sivashankar@msitprogram.net',
            'sksvan.lika@gmail.com','snehathallapaka@gmail.com',
            'sowmyakambam19@gmail.com','sravya2222@gmail.com',
            'sreenath.shivva1992@gmail.com','srinithin7@gmail.com',
            'subadra.koumudi@gmail.com','sudha1993.m@gmail.com',
            'sujatha.girijala496@gmail.com','sunny15593@gmail.com',
            'sureshkumar.palepu@gmail.com','suryateja737@gmail.com',
            'sushee.kalyani@gmail.com','sweetharshu06@gmail.com',
            'tejaswi72minnu@gmail.com','udaykiran0528@gmail.com',
            'venkatesh.2636@gmail.com','vsurajteja1@gmail.com',
            'vyshnavi.nv29@gmail.com','yeswanth.bhoomireddy@gmail.com',
            'ylalithvarma.me@gmail.com']

url = "http://student-monitor.appspot.com/details/taskwise"
with open('data1.csv','wb') as csvfile:
    fieldnames = ["StudentMail"]
    data = urllib.urlencode({"email":'akella.keerthi@gmail.com'})
    resp = urllib.urlopen(url,data)
    #print(resp.read())
    result = json.loads(resp.read())
    dataa=result["data"]
    count=0
    for row in dataa:
        fieldnames.append(row['meta'])
        fieldnames.append(row['meta']+" "+"Key")
        fieldnames.append(row['meta']+" "+"Input")
        fieldnames.append(row['meta']+" "+"Mouse")
    header_row=sorted(fieldnames)
    writer = csv.DictWriter(csvfile,fieldnames = header_row)
    writer.writeheader()
    for mail in students:
        data = urllib.urlencode({"email":mail})
        resp = urllib.urlopen(url,data)
        result = json.loads(resp.read())
        dataa=result["data"]   
        d={"StudentMail":mail}
        for row in dataa:
            if len(row['duration'])>2:
                print(row['duration'])
                duration = str(row['duration']).split(":")
                duration_seconds=((int(duration[0]))*3600)+((int(duration[1]))*60)+int(duration[2])
                d[row['meta']]=duration_seconds/600
                d[row['meta']+" "+"Key"]=row['Key']
                d[row['meta']+" "+"Mouse"]=row['Mouse']
                d[row['meta']+" "+"Input"]=row['Input']
            else:
                d[row['meta']]=0
                d[row['meta']+" "+"Key"]=0
                d[row['meta']+" "+"Input"]=0
                d[row['meta']+" "+"Mouse"]=0
        writer.writerow(d)
        print(mail)
        count=count+1
        if count>4:
            break;
        
