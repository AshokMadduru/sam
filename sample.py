import datetime
from urlparse import urlparse
from httplib import HTTPConnection
import urllib
import json

url = "http://student-monitor.appspot.com/getuserdata"
data = urllib.urlencode({"email":"dasarianvesh100@gmail.com"})
resp = urllib.urlopen(url,data)
#result = json.loads(resp.read())
print(resp.read())
