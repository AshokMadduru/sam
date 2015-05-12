import datetime
from urlparse import urlparse
from httplib import HTTPConnection
import urllib
import json

url = "http://student-monitor.appspot.com/cron/insert"
data = urllib.urlencode({"email":"akella.keerthi@gmail.com"})
resp = urllib.urlopen(url,data)
result = (resp.read())
print(result)
##start_date = datetime.datetime.strptime("27/04/2015 00:00:00",'%d/%m/%Y %H:%M:%S')
##next_date = start_date+datetime.timedelta(days = 1)
##print(type(datetime.datetime.strftime(next_date.date(),"%d/%m/%Y")))
##print(datetime.date.today())
