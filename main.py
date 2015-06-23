"""
Main.py file handles 
"""

## Imports section
###############################
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

from Intermediate import Student,student_key,Url,eventData
from Intermediate import Students,students_key,URL
from Duration import DayDuration
###############################

# Setting up the Jinja environment to include html pages as templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

NAME = "chrome_data"
def browser_key(browser_name = NAME):
    """
    defines a key for Browser entity
    """
    return ndb.Key('Browser',browser_name)

class Chrome(ndb.Model):
    """
    Chrome Model defines Chrome Object(table) with email, eventType, urlLInk,
    datas and timeStamp as properties
    """
    # Email id is a key
    email = ndb.StringProperty(indexed = True)
    eventType = ndb.StringProperty(indexed = False)
    urlLink = ndb.StringProperty(indexed = True)
    datas = ndb.StringProperty(indexed = False)
    timeStamp = ndb.StringProperty(indexed = True)

class ChromeData(webapp2.RequestHandler):
    """
    Gets Chrome data and stores it in Chrome table.It's url is matched
    to "/chrome".
    Input: Mailid, eventype,url, datas and date
    output: Success response if sucess otherwise failure response
    """
    def post(self):
        """
        will be called when /chrome is invoked.
        """
        mail = self.request.get("email")
        eventType = self.request.get("eventType")
        url_link = self.request.get("urlLink")
        datass = self.request.get("datas")
        date = self.request.get("timeStamp")

        # if mail is present store data otherwise ignore
        if mail is not None:
            try:
                #use ndb to store data
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

def pyKeyLogger_key(logger_name = "pyKey"):
    """
    returns key for PyKeyLogger table
    """
    return ndb.Key('PyKey',logger_name)

class PyKeyLogger(ndb.Model):
    """
    Model for PyKeyLogger objec(table) with the folowwing properties
    """
    userName = ndb.StringProperty(indexed = True)
    loggeduser = ndb.StringProperty(indexed = False)
    windowtitle = ndb.StringProperty(indexed = False)
    datas = ndb.StringProperty(indexed = False)
    timeStamp = ndb.StringProperty(indexed = False)

class KeyData(webapp2.RequestHandler):
    """
    KeyData class to store pykeylogger data into datastore.
    Will be called when "/keydata" is invoked.
    """
    def post(self):
        """
        will be first invoked when class is called
        """
        username = self.request.get("user")
        loggeUser = self.request.get("logged")
        title = self.request.get("title")
        datass = self.request.get("datas")
        date = self.request.get("start")
        # Don't store if username is None
        if username is not None:
            try:
                keylogger = self.request.get('logger_name',"pyKey")
                data = PyKeyLogger(parent = pyKeyLogger_key(keylogger))
                data.userName = username
                data.loggeduser = loggeUser
                data.windowtitle = title
                data.datas = datass
                data.timeStamp = date
                data.put()
                self.response.write('Responding...')
            except Exception,e:
                self.response.write(str(e))
        else:
            self.response.write('Failed')

class MainPage(webapp2.RequestHandler):
    """
    Invocation: "/"
    Shows the Home page
    """
    def get(self):
        #get home page from static files and show it as response.
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))

class getPyData(webapp2.RequestHandler):
    """
    Invocation: "/getpydata"
    Returns Pykeylogger data.
    """
    def post(self):
        username = self.request.get("user")
        if username is not None:
            try:
                pykeydata = self.request.get('logger_name',"pyKey")
                qry = PyKeyLogger.query(ancestor = pyKeyLogger_key(pykeydata))
                data_query = qry.filter(PyKeyLogger.userName == username)
                dataa = data_query.fetch()

                result = []
                for row in dataa:
                    result.append(row)
                chrome_data= {}
                chrome_data['data'] = result
                self.response.write(json.dumps(chrome_data))
            except Exception,e:
                self.response.write("error while retrieving: "+str(e))
        else:
            self.response.write('invalid input')

class getChrome(webapp2.RequestHandler):
    """
    Called when: "/gechromedata" 
    """
    def get(self):
        # Show the Student email form named as sample.html
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('sample.html')
        self.response.write(template.render(template_values))

class GetMail(webapp2.RequestHandler):
    """
    Called from: "/getMail"
    Called by: Sample.html when user clicked on submit.
    Output: send dictionary contains students data to studentdata.html
    """
    def post(self):
        mail = self.request.get("email")
        if mail is not None and '@'in mail:
            d = str(datetime.date.today())
            dt = d[-2:]+'/'+d[5:7]+'/'+d[:4]+' 00:00:00'
            try:
                qry = "SELECT * FROM Student WHERE email='"+mail+"""'
                        AND uRl.eventdata.eventTime>'"""+dt+"'"
                data_query = ndb.gql(qry)
                data = data_query.fetch()
                global result
                result = []
                for row in data:
                    temp = {}
                    temp['timestamp'] = row.uRl.eventdata.eventTime
                    temp['url'] = row.uRl.url
                    temp['eventtype'] = row.uRl.eventdata.eventtype
                    temp['eventdata'] = row.uRl.eventdata.eventData
                    result.append(temp)
                #send data to html as template values
                template_values = {'data':result,'name':mail}
                template = JINJA_ENVIRONMENT.get_template('studentdata.html')
                self.response.write(template.render(template_values))
            except Exception,e:
                self.response.write("Error : "+str(e))
        else:
            self.response.write('invalid email')

class GetUsers(webapp2.RequestHandler):
    """
    Called from: "/getusers"
    Output: Dictionary containing unique Students
    """
    def post(self):
        try:
            chromedata = self.request.get('browser_name',"chrome_data")
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
                        userName = row.email[:row.email.find('@')]
                        
                        qry = "SELECT * FROM DayDuration WHERE email='"+row.email+"'"
                        duration_query = ndb.gql(qry)
                        duration = duration_query.fetch()
                        data_dict = {} 
                        for row in duration:
                            data_dict[row.date] = row.duration
                        html = html + "<tr><td>"+str(count)+"""</td><td><a href = http://student-monitor.appspot.com/details/studentdetails?email="""+row.email+" target = _blank>"+userName+"</a></td>"
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

class Dash(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("dash.html")
        self.response.write(template.render())
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/chrome',ChromeData),
    ('/keydata',KeyData),
    ('/getpydata',getPyData),
    ('/getchromedata',getChrome),
    ('/getMail',GetMail),
    ('/getusers',GetUsers),
    ('/dashboard',DashBoard),
    ('/dash',Dash),
], debug=True)
