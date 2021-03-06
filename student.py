import webapp2
import jinja2
import os
import datetime
import json

from google.appengine.ext import ndb
# import Chrome modle from main file
from main import Chrome,browser_key
from Intermediate import Student,student_key,eventData,Url,Student
from Meta import Meta,metaData_key
from Duration import DayDuration



# Setting up the Jinja environment to include html pages as templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

## Student class to show the student home page
class StudenT(webapp2.RequestHandler):
    def get(self):
        try:
            template_values = {}
            template = JINJA_ENVIRONMENT.get_template('student.html')
            self.response.write(template.render(template_values))
        except Exception , e:
            self.response.write(str(e))

## Get the email id from student.html. Then retrieve the details
## of that email id in timestampt sorted order
class GetEmail(webapp2.RequestHandler):
    def get(self):
        try:
            mail = self.request.get("email")

            qry = "SELECT * FROM Meta ORDER BY chapter,moduleNo"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            result = []
            for row in data:
                chro = self.request.get('browser_name','chrome_data')
                qry = Chrome.query(ancestor = browser_key(chro))
                qry1 = qry.filter(Chrome.email == mail)
                qry2 = qry1.filter(Chrome.urlLink == row.url)
                chro_data = qry2.fetch()

                stu = self.request.get('student','student')
                qry = Student.query(ancestor = student_key(stu))
                qry1 = qry.filter(Student.email == mail)
                qry2 = qry1.filter(Student.uRl.url == row.url)
                stu_data = qry2.fetch()

                if len(chro_data) != 0 or len(stu_data) != 0:
                    result.append([row.chapter,row.moduleNo,row.title,
                                row.moduleType,"Visited"])
                else:
                    result.append([row.chapter,row.moduleNo,row.title,
                                row.moduleType," "])
            template_values = {'name':mail,'data':result}
            template = JINJA_ENVIRONMENT.get_template('studentstatus.html')
            self.response.write(template.render(template_values))
        except Exception,e:
            self.response.write(str(e))
app = webapp2.WSGIApplication([
    ('/student/getEmail',GetEmail),
    ('/student/', StudenT),
    ],debug = True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
