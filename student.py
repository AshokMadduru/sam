import webapp2
import jinja2
import os
import datetime
import json

from google.appengine.ext import ndb
# import Chrome modle from main file
from main import Chrome
from Intermediate import Student,student_key,eventData,Url,Student
from Meta import Meta,metaData_key
from Duration import DayDuration



# Setting up the Jinja environment to include html pages as templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

## Student class to show the student home page
class Student(webapp2.RequestHandler):
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

            qry = "SELECT urlLink,timeStamp FROM Chrome WHERE email='"+mail+"' ORDER BY timeStamp DESC"
            data_query = ndb.gql(qry)
            data = data_query.fetch()

            global result_list
            result_list ={}
            global url
            global start_time
            global end_time
            global duration
            global count
            count = 0
            global dataLength
            dataLength = len(data)
            
            for row in data:
                uRl = row.urlLink
                time = row.timeStamp
                if count == 0:
                    url = uRl
                    start_time = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                elif count == dataLength-1:
                    end_time = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                    duration = start_time - end_time
                    if url in result_list:
                        result_list[url][0] = result_list[url][0]+duration
                    else:
                        result_list[url] = [duration,start_time]
                else:
                    end_time = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                    if uRl != url:
                        duration = start_time - end_time
                        if url in result_list:
                            result_list[url][0] = result_list[url][0]+duration
                        else:
                            result_list[url] = [duration,start_time]
                        url = uRl
                        start_time = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                count = count+1
            table_2 = "SELECT * FROM Student WHERE email='"+mail+"""'
                        ORDER BY uRl.eventdata.eventTime DESC"""
            table_2_qry = ndb.gql(table_2)
            table_2_data = table_2_qry.fetch()
            global urll
            global start_timee
            global end_timee
            global durationn
            global countt
            countt = 0
            global datalength
            datalength = len(table_2_data)
            for row in table_2_data:
                uRl = row.uRl.url
                time = row.uRl.eventdata.eventTime
                if countt == 0:
                    urll = uRl
                    start_timee = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                elif countt == datalength-1:
                    end_timee = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                    durationn = start_timee - end_timee
                    if urll in result_list:
                        result_list[urll][0] = result_list[urll][0]+durationn
                    else:
                        result_list[urll] = [durationn,start_timee]
                else:
                    end_timee = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                    if uRl != urll:
                        durationn = start_timee - end_timee
                        if urll in result_list:
                            result_list[urll][0] = result_list[urll][0]+durationn
                        else:
                            result_list[urll] = [durationn,start_timee]
                        urll = uRl
                        start_timee = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                        
                countt = countt+1
            qry = "SELECT * FROM Meta ORDER BY chapter,moduleNo"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            
            html ="""<html><body><table><tr><th>Chapter</th><th>Module No</th><th>Title</th><th>Type</th><th>Duration</th><th>TimeStamp</th></tr>"""
            for row in data:
                if row.url in result_list:
                    if str(result_list[row.url][0]) == 0:
                        html = html+"<tr color = \"green\"><td>"+row.chapter+"</td><td>"+str(row.moduleNo)+"</td><td>"+row.title+"</td><td>"+row.qtype+"</td><td>"+str(result_list[row.url][0])+"</td><td>"+str(result_list[row.url][1])+"</td></tr>"    
                    else:
                        html = html+"<tr color = \"green\"><td>"+row.chapter+"</td><td>"+str(row.moduleNo)+"</td><td>"+row.title+"</td><td>"+row.qtype+"</td><td>"+str(result_list[row.url][0])+"</td><td>"+str(result_list[row.url][1])+"</td></tr>"    
                else:
                    html = html+"<tr><td>"+row.chapter+"</td><td>"+str(row.moduleNo)+"</td><td>"+row.title+"</td><td>"+row.qtype+"</td><td>0</td</tr>"  
            html = html+"""</table></body></html>"""
            self.response.write(html)
        except Exception,e:
            self.response.write(str(e))

class getSample(webapp2.RequestHandler):
    def get(self):
        try:
            #mail = self.request.get("email")
            qry = """  SELECT uRl.url FROM Student
                            WHERE email='"""+"sowmyakambam19@gmail.com"+"'"
            data_qry = ndb.gql(qry)
            data = data_qry.fetch()
            data_list = []
            for row in data:
                data_list.append([row.uRl.url])
            self.response.write(data_list)
        except Exception,e:
            self.response.write(str(e))
app = webapp2.WSGIApplication([
    ('/student/getEmail',GetEmail),
    ('/student/sample',getSample),
    ('/student/', Student),
    ],debug = True)
