import webapp2
from google.appengine.ext import ndb
import datetime
#from main import Chrome
#from Intermediate import Student,student_key,eventData,Url,Student
#from Meta import Meta,medaData_key

## key for DayDuration
def duration_key(key_name = "duration"):
    return ndb.Key("Duration",key_name)
## Day wise duration database
class DayDuration(ndb.Model):
    email = ndb.StringProperty(indexed = True)
    date = ndb.StringProperty(indexed = True)
    startTime = ndb.StringProperty(indexed = True)
    endTime = ndb.StringProperty(indexed = True)
    duration = ndb.StringProperty(indexed = False)

##app = webapp2.WSGIApplication([
##    ('/duration/insert',Manual),
##    ],debug = True)
