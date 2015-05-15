## MentorWise Dashboard

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

## Showing student data mentorwise
class MentorWise(webapp2.RequestHandler):
    def get(self):
##        meta_qry = "SELECT * FROM Meta"
##        meta_data = ndb.gql(meta_qry).fetch()
##        chapterWise = {}
##        for row in meta_data:
##            if row.chapter in chapterWise:
##                chapterWise[row.chapter].append(row.url)
##            else:
##                chapterWise[row.chapter] = [row.url]

        qry = "SELECT * FROM StudentDetails"
        data = ndb.gql(qry).fetch()
        mentors = {}
        for record in data:
            if record.mentor_name in mentors:
##                chap = []
##                for row in chapterWise:
##                    count = 0
##                    for url in chapterWise[row]:
##                        chro = self.request.get('browser_name','chrome_data')
##                        qry = Chrome.query(ancestor = browser_key(chro))
##                        qry1 = qry.filter(Chrome.email == record.student_email)
##                        chro_data = qry1.fetch()
##
##                        stu = self.request.get('student','student')
##                        qry = Student.query(ancestor = student_key(stu))
##                        qry1 = qry.filter(Student.email == record.student_email)
##                        stu_data = qry1.fetch()
##
##                        if len(chro_data) != 0 or len(stu_data) != 0:
##                            count = count+1
##                    
##                    chap.append([chapterWise[row],count])
                mentors[record.mentor_name].append([record.student_name,
                                                    record.student_email])
            else:
##                chap = []
##                for row in chapterWise:
##                    count = 0
##                    for url in chapterWise[row]:
##                        chro = self.request.get('browser_name','chrome_data')
##                        qry = Chrome.query(ancestor = browser_key(chro))
##                        qry1 = qry.filter(Chrome.email == record.student_email)
##                        chro_data = qry1.fetch()
##
##                        stu = self.request.get('student','student')
##                        qry = Student.query(ancestor = student_key(stu))
##                        qry1 = qry.filter(Student.email == record.student_email)
##                        stu_data = qry1.fetch()
##
##                        if len(chro_data) != 0 or len(stu_data) != 0:
##                            count = count+1
##                    
##                    chap.append([chapterWise[row],count])
                mentors[record.mentor_name] = [[record.student_name,
                                                    record.student_email]]
        html = """ <!DOCTYPE html>
<html lang = "en" >
	<head>
		<meta charset = "utf-8">
		<meta http-equiv = "X-UA-Compatible" content = "IE-edge">
		<meta name = "viewport" content = "width=device-width, initial-scale=1">
		<!-- Bootstrap -->
		<link type = "text/css" href = "/bootstrap/bootstrap.min.css" rel = "stylesheet">
	</head>
	<body>
		<div class="container">
			<div class = "row">
				<div class = "col-md-12"> """
        for record in mentors:
            html = html+ "<h1>"+record+"</h1><ol>"
            for row in mentors[record]:
                html = html+ "<li><a href = /student/getEmail?email="+row[1]+" target = _blank>"+row[0]+"</a></li>"
                
            html = html+"</ol>"
        html = html+ """</div>
			</div>
		</div>
		<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    	<!-- Include all compiled plugins (below), or include individual files as needed -->
    	<script src="/bootstrap/bootstrap.min.js"></script>
	</body>
</html> """
        self.response.write(html)

app = webapp2.WSGIApplication([
    ('/mentor/',MentorWise),
    ],debug = True)
