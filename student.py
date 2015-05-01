import webapp2
import jinja2
import os
import datetime
import json

from google.appengine.ext import ndb
# import Chrome modle from main file
from main import Chrome,Meta



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

            d = str(datetime.date.today())
            dt = d[-2:]+'/'+d[5:7]+'/'+d[:4]+' 00:00:00'

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
                    duration = start_time - datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                    if url in result_list:
                        result_list[url] = result_list[url]+duration
                    else:
                        result_list[url] = duration
                else:
                    if uRl != url:
                        duration = start_time - datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                        if url in result_list:
                            result_list[url] = result_list[url]+duration
                        else:
                            result_list[url] = duration
                        url = uRl
                        start_time = datetime.datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                count = count+1
            qry = "SELECT * FROM Meta ORDER BY chapter"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            
            html ="""<html><body><table><tr><th>Chapter</th><th>Title</th><th>Url</th><th>Type</th><th>Duration</th></tr>"""
            for row in data:
                if row.url in result_list:
                    html = html+"<tr><td>"+row.chapter+"</td><td>"+row.title+"</td><td>"+row.url+"</td><td>"+row.type+"</td><td>"+str(result_list[row.url])+"</td</tr>"    
                else:
                    html = html+"<tr><td>"+row.chapter+"</td><td>"+row.title+"</td><td>"+row.url+"</td><td>"+row.type+"</td><td>0</td</tr>"  
            html = html+"""</table></body></html>"""
            self.response.write(html)
        except Exception,e:
            self.response.write(str(e))
            
app = webapp2.WSGIApplication([
    ('/student/', Student),
    ('/student/getEmail',GetEmail)
    ],debug = True)
