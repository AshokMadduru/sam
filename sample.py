import datetime
from urlparse import urlparse
from httplib import HTTPConnection
import urllib
import json

url = "http://student-monitor.appspot.com/chrome"
data = urllib.urlencode({"email":"ashok@taramt.com","eventType":"keyboard","urlLink":"www.youtube.com","datas":"hello","timeStamp":"01/05/2015 05:50:00"})
resp = urllib.urlopen(url,data)
result = (resp.read())
print(result)
