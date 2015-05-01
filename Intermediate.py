## For Intermediate data
import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import datetime
import jinja2
import os
import json

# Setting up the Jinja environment to include html pages as templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



## model for student database
def student_key(student = "student"):
    return ndb.Key("StudentData",student)

## model for eventData
class eventData(ndb.Model):
    eventData = ndb.StringProperty(indexed = False)
    eventTime = ndb.StringProperty(indexed = True)
    eventtype = ndb.StringProperty(indexed = False)

## model for url
class Url(ndb.Model):
    url = ndb.StringProperty(indexed = True)
    eventdata = ndb.StructuredProperty(eventData)
## model for student
class Student(ndb.Model):
    email = ndb.StringProperty(indexed = True)
    uRl = ndb.StructuredProperty(Url)



class Hai(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get("email")
        eventType = self.request.get("eventType")
        url_link = self.request.get("urlLink")
        data = self.request.get("datas")
        date = self.request.get("timeStamp")
        if mail is not None:
            try:
                stu = self.request.get('student',"student")
                student = Student(parent = student_key(stu))
                student.email = mail
                student.uRl = Url(url = url_link,
                    eventdata = eventData(eventData = data,
                                          eventTime = date,
                                          eventtype = eventType))

                student.put()
                self.response.write('success')
            except Exception, e:
                self.response.write(str(e))
        else:
            self.response.write('no')

interm  = webapp2.WSGIApplication([
    ('/interm/hello', Hai),
], debug=True)                        
