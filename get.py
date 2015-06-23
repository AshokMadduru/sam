import csv
import json
import datetime
from urlparse import urlparse
from httplib import HTTPConnection
import urllib

url = "http://student-monitor.appspot.com/student/getEmail"
data = urllib.urlencode({"email":"akella.keerthi@gmail.com"})
resp = urllib.urlopen(url,data)
result = json.loads(resp.read())
print(type(result))
#print(result['data'][0])
##with open('data.csv','w') as csvfile:
##    fieldnames = ['URL','Duration']
##    writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
##    writer.writeheader()
##    for row in result['data']:
##        print(len(row))
##        print(row)
##        print(row[0])
##        writer.writerow({'URL':row[0],'Duration':row[1]})
                
