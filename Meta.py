import webapp2
from google.appengine.ext import ndb

import datetime
import jinja2
import os
import json

import cgi
import urllib

## Generating key for metadata
def metaData_key(meta_name = "meta"):
    return ndb.Key("Meta",meta_name)

## Model for metaData
class Meta(ndb.Model):
    chapter = ndb.StringProperty(indexed = True)
    moduleNo = ndb.IntegerProperty(indexed = True)
    url = ndb.StringProperty(indexed = True)
    title = ndb.StringProperty(indexed = False)
    moduleType = ndb.StringProperty(indexed = False)
    qtype = ndb.StringProperty(indexed = False)
    duration = ndb.StringProperty(indexed = False)

## class for storing metadata
class StoreMeta(webapp2.RequestHandler):
    def post(self):
        chap = self.request.get("chapter")
        module = self.request.get("moduleno")
        uRl = self.request.get("url")
        tiTle = self.request.get("title")
        tyPe = self.request.get("type")
        duRation = self.request.get("duration")
        quizType = self.request.get("qtype")
        if uRl is not None :
            try:
                data = Meta(chapter = chap, moduleNo = int(module),
                            url = uRl, title = tiTle,
                            moduleType = tyPe,
                            qtype = quizType, duration = duRation)
                data.put()
                self.response.write("success")
            except Exception, e:
                self.response.write(str(e))
        else:
            self.response.write("failed")

# key for student-mentor darabase
def student_assignedData_key(name = 'assigned'):
    return ndb.Key('StudentDetails',name)
## Model for Student Details
class StudentDetails(ndb.Model):
    student_name = ndb.StringProperty(indexed = True)
    student_email = ndb.StringProperty(indexed = True)
    student_id = ndb.StringProperty(indexed = True)
    mentor_name = ndb.StringProperty(indexed = True)

class InsertStudentDetails(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        mail = self.request.get('mail')
        stuId = self.request.get('stuid')
        mentor = self.request.get('mentor')

        data = StudentDetails(student_name = name,student_email = mail,
                             student_id = stuId,mentor_name = mentor )
        try:
            data.put()
            self.response.write('success')
        except Exception,e:
            self.response.write(str(e))

##class GetStudentDetails(webapp2.RequestHandler):
##    def getstudents(self):
##        stu = self.request.get('name','assigned')
##        qry = StudentDetails.query(ancestor = student_assignedData_key(stu))
##        data = qry.fetch()
##        return data
            
app = webapp2.WSGIApplication([
    ('/meta/insert',StoreMeta),
    ('/meta/insertstu',InsertStudentDetails),
    ],debug = True)
