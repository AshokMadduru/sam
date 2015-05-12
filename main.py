import sys
import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import datetime
import jinja2
import os
import json
import datetime

from Intermediate import Student,student_key,Url,eventData
from Intermediate import Students,students_key,URL
from Duration import DayDuration

# Setting up the Jinja environment to include html pages as templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

## Define a key for chrome Entity
NAME = "chrome_data"
def browser_key(browser_name = NAME):
    return ndb.Key('Browser',browser_name)

## Define email, eventType, urlLink, data and timeStamp as properties of Chrome Entity.
class Chrome(ndb.Model):
    # Email id is a key
    email = ndb.StringProperty(indexed = True)
    eventType = ndb.StringProperty(indexed = False)
    urlLink = ndb.StringProperty(indexed = True)
    datas = ndb.StringProperty(indexed = False)
    timeStamp = ndb.StringProperty(indexed = True)

## Getting chrome data and storing in the database.
class ChromeData(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get("email")
        eventType = self.request.get("eventType")
        url_link = self.request.get("urlLink")
        datass = self.request.get("datas")
        date = self.request.get("timeStamp")
        if mail is not None:
            try:
                stu = self.request.get('student',"student")
                student = Student(parent = student_key(stu))
                student.email = mail
                student.uRl = Url(url = url_link,
                    eventdata = eventData(eventData = datass,
                                          eventTime = date,
                                          eventtype = eventType))

                student.put()
                self.response.write('success')
            except Exception, e:
                self.response.write(str(e))
        else:
            self.response.write('no')
        self.response.write('Success...')

# defining the key for PyKeyLogger entity
def pyKeyLogger_key(logger_name = "pyKey"):
    return ndb.Key('PyKey',logger_name)

## Define userName, loggeduser, windowtitle, datas and timeStamp as properties of
## PyKeyLogger Entity.
class PyKeyLogger(ndb.Model):
    userName = ndb.StringProperty(indexed = True)
    loggeduser = ndb.StringProperty(indexed = False)
    windowtitle = ndb.StringProperty(indexed = False)
    datas = ndb.StringProperty(indexed = False)
    timeStamp = ndb.StringProperty(indexed = False)

class KeyData(webapp2.RequestHandler):
    def post(self):   
        username = self.request.get("user")
        loggeUser = self.request.get("logged")
        title = self.request.get("title")
        datass = self.request.get("datas")
        date = self.request.get("start")
        if username is not None:
            keylogger = self.request.get('logger_name',"pyKey")
            data = PyKeyLogger(parent = pyKeyLogger_key(keylogger))
            data.userName = username
            data.loggeduser = loggeUser
            data.windowtitle = title
            data.datas = datass
            data.timeStamp = date
            data.put()
        else:
            self.response.write('no')
        self.response.write('Responding...')
class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.write('Hello world!')
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))

class getPyData(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("user")
        pykeydata = self.request.get('logger_name',"pyKey")
        qry = PyKeyLogger.query(ancestor = pyKeyLogger_key(pykeydata))
        data_query = qry.filter(PyKeyLogger.userName == username)
        dataa = data_query.fetch()
        global result
        result = []
        for row in dataa:
            result.append(row)
        chrome_data= {}
        chrome_data['data'] = result
        self.response.write(result[0])

class getChrome(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('sample.html')
        self.response.write(template.render(template_values))

HTML = """\
<html>
  <body>
    <div>
        <table>
            <tr><th>TimeStamp</th><th>eventType</th><th>url</th><th>data</th></tr>
        
"""
class GetMail(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get("email")

        d = str(datetime.date.today())
        dt = d[-2:]+'/'+d[5:7]+'/'+d[:4]+' 00:00:00'

        qry = "SELECT * FROM Student WHERE email='"+mail+"""'
                        AND uRl.eventdata.eventTime>'"""+dt+"'"## ORDER BY timeStamp DESC"
        data_query = ndb.gql(qry)
        data = data_query.fetch()
            
        global result
        result = []
        global HTML
        HTML = """\
        <html>
          <body border=\"1\" style=\"width:100%\">
            <div>
            <table>
            <tr><th>TimeStamp</th><th>Url</th><th>eventdata</th><th>eventtype</th></tr>
        
        """
        global count
        count = 0
        for row in data:
            HTML = HTML+"<tr><td>"+row.uRl.eventdata.eventTime+"</td><td>"+row.uRl.url+"</td><td>"+row.uRl.eventdata.eventData+"</td><td>"+row.uRl.eventdata.eventtype+"</td></tr>"
        HTML = HTML+"</table></div></body></html>"
        self.response.write(HTML)
        #self.response.write(mail)
class GetUsers(webapp2.RequestHandler):
    def post(self):
        try:
            chromedata = self.request.get('browser_name',"chrome_data")
 ##           qry = Chrome.query(ancestor = browser_key(chromedata))
##            data_query = qry.filter(projection = ['email'], distinct = True)
##            dataa = qry.fetch()
            qry = "SELECT DISTINCT email FROM Chrome"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            global resu
            resu = []
            for row in data:
                if row.email not in resu and '@' in row.email:
                    resu.append(row.email)
            user_list = {'users':resu}
            self.response.write(json.dumps(user_list))
        except Exception , e:
            self.response.write(str(e))
class DashBoard(webapp2.RequestHandler):
    def get(self):
        global html
        html = """\
        <html>
            <head>
                <meta charset = "utf-8">
		<meta http-equiv = "X-UA-Compatible" content = "IE-edge">
		<meta name = "viewport" content = "width=device-width, initial-scale=1">
		<title>DashBoard</title>
		<!-- Bootstrap -->
		<link type = "text/css" href = "/bootstrap/bootstrap.min.css" rel = "stylesheet">
            </head>
          <body><h1>Compilers course</h1><h3>(From Mar-27)</h3>
            <div>
            <table class="table table-striped">
            <tr><th>Sl No</th><th>Student Email</th>
        
        """
        try:
            qry = "SELECT DISTINCT email FROM Chrome"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            global resu
            resu = []
            global count
            count = 1
            today = datetime.date.today()
            start = datetime.datetime.strptime('27-04-2015','%d-%m-%Y').date()
            while(start<today):
                html = html+"<th>"+datetime.datetime.strftime(start,'%d/%m/%Y')[:2]+"</th>"
                start = start+datetime.timedelta(days=1)
            html = html+"</tr>"
            for row in data:
                if row.email not in resu and '@' in row.email:
                    try:
                        qry = "SELECT * FROM DayDuration WHERE email='"+row.email+"'"
                        duration_query = ndb.gql(qry)
                        duration = duration_query.fetch()
                        data_dict = {} 
                        for row in duration:
                            data_dict[row.date] = row.duration
                        html = html + "<tr><td>"+str(count)+"""</td><td><a href = http://student-monitor.appspot.com/student/getEmail?
                                    email="""+row.email+" target = _blank>"+row.email+"</a></td>"
                        start = datetime.datetime.strptime('27-04-2015','%d-%m-%Y').date()
                        while(start<today):
                            if datetime.datetime.strftime(start,'%d/%m/%Y') in data_dict:
                                html = html+"<td>"+data_dict[datetime.datetime.strftime(start,'%d/%m/%Y')][:4]+"</td>"
                            else:
                                html = html+"<td>0</td>"
                            start = start+datetime.timedelta(days=1)
                        html = html+"</tr>"
                    except Exception,e:
                        self.response.write(str(e))            
                count = count+1
            html = html+"""</table></div>
                            <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
                            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
                            <!-- Include all compiled plugins (below), or include individual files as needed -->
                            <script src="/bootstrap/bootstrap.min.js"></script>
                            </body></html>"""
            self.response.write(html)
        except Exception , e:
            self.response.write(str(e))
      
    
class GetUserData(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get("email")
        chromedata = self.request.get('browser_name',"chrome_data")
        qry = Chrome.query(ancestor = browser_key(chromedata))
        data_query = qry.filter(Chrome.email == mail)
        dataa = data_query.fetch()
        global result
        result = []
        for row in dataa:
            temp = {}
            temp['evenType'] = row.eventType
            temp['urlLink'] = row.urlLink
            temp['datas'] = row.datas
            temp['timeStamp'] = row.timeStamp
            temp['email'] = row.email
            result.append(temp)
        chrome_data= {'data':result}
        #self.response.write(HTML)
        self.response.write(json.dumps(chrome_data))

## Define a key for Chapter Entity
def chapter_key(intermediate_key = "chapter_key"):
    return ndb.Key('Chapter',intermediate_key)

## class for timings
class Timings(ndb.Model):
    timings = ndb.StringProperty(indexed = False)
## class for users
class Users(ndb.Model):
    user_mail = ndb.StringProperty(indexed = True)
    count = ndb.IntegerProperty(indexed = False)
    timings = ndb.StructuredProperty(Timings)
## class for url
class UrlLink(ndb.Model):
    url = ndb.StringProperty(indexed = True)
    title = ndb.StringProperty(indexed = False)
    users = ndb.StructuredProperty(Users)
## class for Chapter
class Chapter(ndb.Model):
    chapter = ndb.StringProperty(indexed = True)
    module = ndb.StructuredProperty(UrlLink)
## class for generating intermediate table
class Intermediate(webapp2.RequestHandler):
    def post(self):
        username = self.request.get("user")
        loggeUser = self.request.get("logged")
        title = self.request.get("title")
        datass = self.request.get("datas")
        date = self.request.get("start")



## storing student data
class GetAllUrls(webapp2.RequestHandler):
    def get(self):
        try:
            qry = "SELECT DISTINCT url FROM Meta"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            global htmll
            htmll = """\
            <html>
              <body border=\"1\" style=\"width:100%\"><h1>URL Access History</h1>
                <div>
                <table>
                <tr><th>Sl No</th><th>URL</th><th>Count</th></tr>
        
            """
            global c
            c = 1
            global cc
            cc = 1
            for uRl in data:
                if cc>30:
                    break
                cc =cc +1
                link = uRl.url
                count_qry = "SELECT timeStamp FROM Chrome WHERE urlLink='"+link+"'"
                count_query = ndb.gql(count_qry)
                count_data = count_query.fetch()
                count = 0
                for row in count_data:
                    count = count+1
                htmll = htmll+"<tr><td>"+str(c)+"</td><td>"+link+"</td><td>"+str(count)+"</td></tr>"
                c = c+1
            htmll = htmll+"</table></div></body></html>"
            self.response.write(htmll)
        except Exception ,e:
            self.response.write(str(e))

## Get Url Data
class GetUrlData(webapp2.RequestHandler):
    def get(self):
        chromedata = self.request.get('browser_name',"chrome_data")
        qry = Chrome.query(ancestor = browser_key(chromedata))
        #data_query = qry.filter(Chrome.email == "anveshika.09@gmail.com")
        dataa = qry.fetch()
        result = {}
        count = 0
        for row in dataa:
            count = count + 1
            if count > 1000:
                break
            if (result.has_key(row.urlLink)):
                result[row.urlLink][0] = result[row.urlLink][0] + 1
                result[row.urlLink][1].append(row.email)
                result[row.urlLink][1] = list(set(result[row.urlLink][1]))
            else:
                result[row.urlLink] = [1,[row.email]]
        global HTML
        HTML = """\
        <html>
          <body border=\"1\" style=\"width:100%\">
            <div>
            <table>
            <tr><th>URL</th><th>Count</th><th>Students</th></tr>
        
        """
        for url in result:        
            HTML = HTML+"<tr><td>"+url+"</td><td>"+str(result[url][0])+"</td><td>"+''.join(result[url][1])+"</td</tr>"
        HTML = HTML+"</table></div></body></html>"
        chrome_data= {'data':result}
        self.response.write(HTML)
        #self.response.write(mail)
class getStuData(webapp2.RequestHandler):
    def get(self):
        mail = self.request.get("email")
        self.response.write(mail)
        try:
            qry = "SELECT * FROM Meta ORDER BY chapter"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            HTML = """\
            <html>
              <body border=\"1\" style=\"width:100%\">
                <div>
                <table>
                <tr><th>Chapter</th><th>Title</th><th>Url</th><th>Type</th><th>Count</th></tr>
        
            """
            for row in data:
                url = row.url
                users_qry = "SELECT timeStamp FROM Chrome WHERE email='"+mail+"' AND urlLink='"+url+"'"
                users_data_query = ndb.gql(users_qry)
                users_data = users_data_query.fetch()
                count = 0
                for t in users_data:
                    count = count+1
                HTML = HTML+"<tr><td>"+row.chapter+"</td><td>"+row.title+"</td><td>"+url+"</td><td>"+row.type+"</td><td>"+str(count)+"</td</tr>"
            HTML = HTML+"</table></div></body></html>"
            self.response.write(HTML)
        except Exception, e:
            self.response.write(str(e))
class Dump(webapp2.RequestHandler):
    def post (self):
        mail = 'akella.keerthi@gmail.com'
        if mail is not None:
            try:
                qry = """SELECT * FROM Chrome
                        WHERE email='"""+mail+"'"
                data_query = ndb.gql(qry)
                data = data_query.fetch()
                data_list = []
                count = 0
                for row in data:
                    self.response.write(count)
                    count = count+1
                    data_list.append(URL(url = row.urlLink,eventTime = row.timeStamp))
                details = Students(id = mail, email = mail, uRl = data_list)
                details.put()
                self.response.write('success')
 
            except Exception, e:
                self.response.write(str(e))
        else:
            self.response.write('no')
## Get mail replica changed to mailget
class MailGet(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get("email")
        date1 = self.request.get("date1")
        date2 = self.request.get("date2")

        qry = "SELECT * FROM Student WHERE email='"+mail+"""'
                        AND uRl.eventdata.eventTime>'"""+date1+"' AND uRl.eventdata.eventTime<'"+date2+"'"
        data_query = ndb.gql(qry)
        data = data_query.fetch()
        global count
        global start_time
        global end_time
        count = 0
        for row in data:
            if count == 0:
                start_time = row.uRl.eventdata.eventTime
            elif count == len(data)-1:
                end_time = row.uRl.eventdata.eventTime
            count = count+1
        self.response.write(start_time+" "+end_time)
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/chrome',ChromeData),
    ('/keydata',KeyData),
    ('/getpydata',getPyData),
    ('/getchromedata',getChrome),
    ('/getMail',GetMail),
    ('/getusers',GetUsers),
    ('/getuserdata',GetUserData),
    ('/dashboard',DashBoard),
    ('/geturldata',GetUrlData),
    ('/geturls',GetAllUrls),
    ('/getstudeta',getStuData),
    ('/dump',Dump),
    ('/mailGet',MailGet),
], debug=True)
