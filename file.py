import csv
from urlparse import urlparse
from httplib import HTTPConnection
import urllib
import json
import datetime

with open('Lesson-1 Metadata.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in reader:
        idNo = row[0]
        name = row[1]
        mentor = row[2]
        email = row[3]
        url = "http://student-monitor.appspot.com/meta/insertstu"
        data = urllib.urlencode({"name":name,"mail":email,"stuid":idNo,
                                 "mentor":mentor})
        resp = urllib.urlopen(url,data)
        print(resp.read())
print('completed')
##date = datetime.datetime.strptime('27-04-2015','%d-%m-%Y').date()
##print(date)
##while(date <= datetime.date.today()):
##    date = date +datetime.timedelta(days = 1)
##    print(datetime.datetime.strftime(date,'%d/%m/%Y'))
