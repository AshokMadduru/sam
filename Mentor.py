import webapp2
import jinja2
import datetime
import os

from google.appengine.ext import ndb
from Meta import StudentDetails,student_assignedData_key,metaData_key,Meta
from Intermediate import Student,student_key,Url,eventData
from main import browser_key,Chrome

# Setting up the Jinja environment to include html pages as templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MentorWise(webapp2.RequestHandler):
    def get(self):
        meta_qry = "SELECT * FROM Meta"
        meta_data = ndb.gql(meta_qry).fetch()
        chapterWise = {}
        for row in meta_data:
            if row.chapter in chapterWise:
                chapterWise[row.chapter].append(row.url)
            else:
                chapterWise[row.chapter] = [row.url]

        qry = "SELECT * FROM StudentDetails"
        data = ndb.gql(qry).fetch()
        mentors = {}
        for record in data:
            if record.mentor_name in mentors:
                for row in chapterWise:
                    count = 0
                    for url in chapterWise[row]:
                        chro = self.request.get('browser_name','chrome_data')
                        qry = Chrome.query(ancestor = browser_key(chro))
                        qry1 = qry.filter(Chrome.email == record.student_email)
                        chro_data = qry1.fetch()

                        stu = self.request.get('student','student')
                        qry = Student.query(ancestor = student_key(stu))
                        qry1 = qry.filter(Student.email == mail)
                        stu_data = qry1.fetch()

                        if len(chro_data) != 0 or len(stu_data) != 0:
                            count = count+1
                    
                mentors[record.mentor_name].append([record.student_name,
                                                    record.student_email])
            else:
                mentors[record.mentor_name] = [[record.student_name,
                                                    record.student_id,
                                                    record.student_email]]
        
        template = JINJA_ENVIRONMENT.get_template('mentor.html')
        self.response.write(template.render({'data':mentors}))

app = webapp2.WSGIApplication([
    ('/mentor/',MentorWise),
    ],debug = True)
