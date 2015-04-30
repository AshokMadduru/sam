import datetime
from urlparse import urlparse
from httplib import HTTPConnection
import urllib
import json

##url = "http://student-monitor.appspot.com/getusers"
##data = urllib.urlencode({})
##resp = urllib.urlopen(url,data)
##result = json.loads(resp.read())
d = str(datetime.date.today())
dt = d[-2:]+'/'+d[5:7]+'/'+d[:4]+' 00:00:00'
print(str(type(dt)))
