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

#from main import Chrome

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
    eventData = ndb.StringProperty(indexed = True)
    eventTime = ndb.StringProperty(indexed = True)
    eventtype = ndb.StringProperty(indexed = True)

## model for url
class Url(ndb.Model):
    url = ndb.StringProperty(indexed = True)
    eventdata = ndb.StructuredProperty(eventData)
## model for student
class Student(ndb.Model):
    email = ndb.StringProperty(indexed = True)
    uRl = ndb.StructuredProperty(Url)

########################
########################
def students_key(students = "students"):
    return ndb.Key("Students",students)


class URL(ndb.Model):
    url = ndb.StringProperty(indexed = True)
    eventTime = ndb.StringProperty(indexed = True)

class Students(ndb.Model):
    email = ndb.StringProperty(indexed = True)
    uRl = ndb.StructuredProperty(URL,repeated = True)
class Hello(webapp2.RequestHandler):
    def post (self):
##        mail = self.request.get("email")
##        eventType = self.request.get("eventType")
##        url_link = self.request.get("urlLink")
##        data = self.request.get("datas")
##        date = self.request.get("timeStamp")
        mail = 'akella.keerthi@gmail.com'
        if mail is not None:
            try:
                qry = """SELECT * FROM Chrome
                        WHERE email='"""+mail+"'"
                data_query = ndb.gql(qry)
                data = data_query.fetch()
                data_list = []
                for row in data:
                    data_list.append(URL(url = rpw.urlLink,
                        eventdata = EventData(eventData = row.datas,
                                          eventTime = row.timeStamp,
                                          eventtype = row.eventType)))
                details = Students(id = mail, email = mail, uRl = data_list)
                details.put()
                self.response.write('success')
                #stu = self.request.get('students',"students")
                key = students_key(mail)
##                qry = Students.query(ancestor = key )
##                datas = qry.filter(Students.email == mail)
##                student = Students(parent = students_key(stu),email = mail)
##                stude = datas.fetch()
##                data_list = []
##                for row in stude:
##                    for r in row.uRl:
##                        data_list.append(r)
##                data_list.append(URL(url = url_link,
##                    eventdata = EventData(eventData = data,
##                                          eventTime = date,
##                                          eventtype = eventType)))

##                reco = Students(id = mail,email = mail,uRl=[URL(url = url_link,
##                                        eventdata=EventData(eventData = data,
##                                              eventTime = date,
##                                                eventtype = eventType))])
##                a = reco.put()
                #self.response.write(key.delete())
##                student.uRl = data_list
##                student.put()
##                self.response.write('success')
            except Exception, e:
                self.response.write(str(e))
        else:
            self.response.write('no')

########################
####################

class Hai(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get("email")
        eventType = self.request.get("eventType")
        url_link = self.request.get("urlLink")
        data = self.request.get("datas")
        date = self.request.get("timeStamp")
        if mail is not None:
            try:
##                qry = """INSERT into Student (uRl.url,uRl.
##                                            eventdata.eventData,
##                                            eventdata.eventTime,
##                                            eventdata.eventType)
##                        VALUES ("""+urlLink+","+data+","+date+","+eventType+""")
##                        WHERE email='"""+mail"'"
                stu = self.request.get('student',"student")
                student = Student(parent = student_key(stu),email = mail)
                student.uRl = Url(url = url_link,
                    eventdata = eventData(eventData = data,
                                          eventTime = date,
                                          eventtype = eventType))

                student.put()
##                ndb.gql(qry)
                self.response.write('success')
            except Exception, e:
                self.response.write(str(e))
        else:
            self.response.write('no')

interm  = webapp2.WSGIApplication([
    ('/interm/he',Hello),
    ('/interm/hello', Hai),
], debug=True)                        
