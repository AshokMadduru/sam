#################################
import webapp2
import datetime
import jinja2
import os
import json

from google.appengine.ext import ndb
from Intermediate import Student,student_key,Url,eventData
from main import browser_key,Chrome
from Meta import metaData_key,Meta

#################################

# Setting up the Jinja environment to include html pages as templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class DetailsHome(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('details.html')
        self.response.write(template.render())

class StudentDetails(webapp2.RequestHandler):
    def get(self):
        mail = self.request.get("email")
        if mail is not None and '@' in mail:
            self.result_student_data=[]
            self.meta_data = {}
            self.getMetaData()
            start_date = datetime.datetime.strptime('27/04/2015 08:30:00',
                                                    '%d/%m/%Y %H:%M:%S')
            while(start_date<datetime.datetime.now()):
                start_time_str = datetime.datetime.strftime(start_date,
                                                            '%d/%m/%Y %H:%M:%S')
                end_time = start_date+datetime.timedelta(hours=12)
                end_time_str = datetime.datetime.strftime(end_time,
                                                          '%d/%m/%Y %H:%M:%S')
                self.student_data = []
                self.getFirstTableData(mail,start_time_str,end_time_str)
                self.getSecondTableData(mail,start_time_str,end_time_str)
                result = []
                for record in self.student_data:
                    if 'udacity' in record[1]:
                        if record[1] in self.meta_data:
                            urlData = self.meta_data[record[1]]
                            chapter = urlData[0]
                            moduleNo = urlData[1]
                            title = urlData[2]
                            moduleType = urlData[3]
                            result.append([record[0],chapter,moduleNo,
                                           title,moduleType])
                        else:
                            result.append([record[0],'Udacity'," ",
                                           " ","Discussions"])
                    else:
                        domainName = self.getDomain(record[1])
                        if domainName != 'ignore':
                            result.append([record[0],domainName," "," "
                                             ," "])
                self.getDuration(result)
                start_date = end_time+datetime.timedelta(hours=12)
            template_values = {'name':mail,'data':self.result_student_data}
            template = JINJA_ENVIRONMENT.get_template('studentdetails.html')
            self.response.write(template.render(template_values))
        else:
            self.response.write('check your mail')

    def getFirstTableData(self,mail,time_stamp1,time_stamp2):
        try:
            # Get data from Chrome Table
            chro = self.request.get('browser_name','chrome_data')
            qry = Chrome.query(ancestor = browser_key(chro))
            qry1 = qry.filter(Chrome.email == mail)
            qry2 = qry1.filter(Chrome.timeStamp >=time_stamp1)
            qry3 = qry2.filter(Chrome.timeStamp <time_stamp2)
            data = qry3.fetch()
            result = []
            last = " "
            for record in data:
                if record.timeStamp != last:
                    self.student_data.append([record.timeStamp,
                                              record.urlLink])
                    last = record.timeStamp
            return 
        except Exception,e:
            self.response.write('unable to get data'+str(e))

    def getSecondTableData(self,mail,time_stamp1,time_stamp2):
        try:
            # get data from Student table
            stu = self.request.get('student','student')
            qry = Student.query(ancestor = student_key(stu))
            qry1 = qry.filter(Student.email == mail)
            qry2 = qry1.filter(Student.uRl.eventdata.eventTime >=time_stamp1)
            qry3 = qry2.filter(Student.uRl.eventdata.eventTime <time_stamp2)
            data = qry3.fetch()
            result = []
            last = " "
            for row in data:
                if row.uRl.eventdata.eventTime !=last:
                    self.student_data.append([row.uRl.eventdata.eventTime,
                                   row.uRl.url])
                    last = row.uRl.eventdata.eventTime
            return 
        except Exception,e:
            self.response.write('unable to get data '+str(e))

    def getMetaData(self):
        try:
            qry = "SELECT * FROM Meta ORDER BY chapter,moduleNo"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            for record in data:
                self.meta_data[record.url] = [record.chapter,record.moduleNo,
                                              record.title,record.moduleType,
                                              record.qtype,record.duration]
            return 
        except Exception,e:
            self.response.write('unable to get data '+str(e))

    def getDomain(self,url):
        if url is not None or url is not "" or url is not " ":
            if '//' in url:
                first_index = url.index('//')
                if 'www' in url[first_index+2:]:
                    pos_of_second_dot = url[url.index('www')+4:].index('.')
                    return url[url.index('www')+4:
                               url.index('www')+4+pos_of_second_dot]
                else:
                    if '.' in url[first_index+2:]:
                        pos_of_dot = url[first_index+2:].index('.')
                        return url[first_index+2:first_index+2+pos_of_dot]
                    else:
                        return url[first_index+2:]
            else:
                if '.' in url:
                    return url[:url.index('.')]
                else:
                    return url
        else:
            return 'ignore'

    def getDuration(self,data):
        count = 0
        result = []
        while(count<len(data)-1):
            first = datetime.datetime.strptime(data[count][0],
                                               '%d/%m/%Y %H:%M:%S')
            second = datetime.datetime.strptime(data[count+1][0],
                                                '%d/%m/%Y %H:%M:%S')
            duration = second-first
            self.result_student_data.append([data[count][0],data[count][1],
                                        data[count][2],data[count][3],
                                        data[count][4],str(duration)])
            count = count+1
        #self.result_student_data.append([data[count][0],data[count][1],
                                       #  data[count][2],data[count][3],
                                        # data[count][4]," "])
        return 

class TaskWiseData(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get("email")
        if mail is not None and '@' in mail:
            self.result_student_data=[]
            self.meta_data = {}
            self.getMetaData()
            start_date = datetime.datetime.strptime('27/04/2015 08:30:00',
                                                    '%d/%m/%Y %H:%M:%S')
            while(start_date<datetime.datetime.now()):
                start_time_str = datetime.datetime.strftime(start_date,
                                                            '%d/%m/%Y %H:%M:%S')
                end_time = start_date+datetime.timedelta(hours=12)
                end_time_str = datetime.datetime.strftime(end_time,
                                                          '%d/%m/%Y %H:%M:%S')
                self.student_data = []
                self.getFirstTableData(mail,start_time_str,end_time_str)
                self.getSecondTableData(mail,start_time_str,end_time_str)
                result = []
                for record in self.student_data:
                    if 'udacity' in record[1]:
                        if record[1] in self.meta_data:
                            urlData = self.meta_data[record[1]]
                            chapter = urlData[0]
                            moduleNo = urlData[1]
                            title = urlData[2]
                            moduleType = urlData[3]
                            result.append([record[0],chapter,moduleNo,
                                           title,moduleType])
                        else:
                            result.append([record[0],'Udacity'," ",
                                           " ","Discussions"])
                    else:
                        domainName = self.getDomain(record[1])
                        if domainName != 'ignore':
                            result.append([record[0],domainName," "," "
                                             ," "])
                self.getDuration(result)
                start_date = end_time+datetime.timedelta(hours=12)
            template_values = {'name':mail,'data':self.result_student_data}
            template = JINJA_ENVIRONMENT.get_template('studentdetails.html')
            self.response.write(self.result_student_data)
        else:
            self.response.write('check your mail')

    def getFirstTableData(self,mail,time_stamp1,time_stamp2):
        try:
            # Get data from Chrome Table
            chro = self.request.get('browser_name','chrome_data')
            qry = Chrome.query(ancestor = browser_key(chro))
            qry1 = qry.filter(Chrome.email == mail)
            qry2 = qry1.filter(Chrome.timeStamp >=time_stamp1)
            qry3 = qry2.filter(Chrome.timeStamp <time_stamp2)
            data = qry3.fetch()
            result = []
            last = " "
            for record in data:
                if record.timeStamp != last:
                    self.student_data.append([record.timeStamp,
                                              record.urlLink])
                    last = record.timeStamp
            return 
        except Exception,e:
            self.response.write('unable to get data'+str(e))

    def getSecondTableData(self,mail,time_stamp1,time_stamp2):
        try:
            # get data from Student table
            stu = self.request.get('student','student')
            qry = Student.query(ancestor = student_key(stu))
            qry1 = qry.filter(Student.email == mail)
            qry2 = qry1.filter(Student.uRl.eventdata.eventTime >=time_stamp1)
            qry3 = qry2.filter(Student.uRl.eventdata.eventTime <time_stamp2)
            data = qry3.fetch()
            result = []
            last = " "
            for row in data:
                if row.uRl.eventdata.eventTime !=last:
                    self.student_data.append([row.uRl.eventdata.eventTime,
                                   row.uRl.url])
                    last = row.uRl.eventdata.eventTime
            return 
        except Exception,e:
            self.response.write('unable to get data '+str(e))

    def getMetaData(self):
        try:
            qry = "SELECT * FROM Meta ORDER BY chapter,moduleNo"
            data_query = ndb.gql(qry)
            data = data_query.fetch()
            for record in data:
                self.meta_data[record.url] = [record.chapter,record.moduleNo,
                                              record.title,record.moduleType,
                                              record.qtype,record.duration]
            return 
        except Exception,e:
            self.response.write('unable to get data '+str(e))

    def getDomain(self,url):
        if url is not None or url is not "" or url is not " ":
            if '//' in url:
                first_index = url.index('//')
                if 'www' in url[first_index+2:]:
                    pos_of_second_dot = url[url.index('www')+4:].index('.')
                    return url[url.index('www')+4:
                               url.index('www')+4+pos_of_second_dot]
                else:
                    if '.' in url[first_index+2:]:
                        pos_of_dot = url[first_index+2:].index('.')
                        return url[first_index+2:first_index+2+pos_of_dot]
                    else:
                        return url[first_index+2:]
            else:
                if '.' in url:
                    return url[:url.index('.')]
                else:
                    return url
        else:
            return 'ignore'

    def getDuration(self,data):
        count = 0
        result = []
        while(count<len(data)-1):
            first = datetime.datetime.strptime(data[count][0],
                                               '%d/%m/%Y %H:%M:%S')
            second = datetime.datetime.strptime(data[count+1][0],
                                                '%d/%m/%Y %H:%M:%S')
            duration = second-first
            self.result_student_data.append([data[count][0],data[count][1],
                                        data[count][2],data[count][3],
                                        data[count][4],str(duration)])
            count = count+1
        #self.result_student_data.append([data[count][0],data[count][1],
                                       #  data[count][2],data[count][3],
                                        # data[count][4]," "])
        return                           
app = webapp2.WSGIApplication([
    ('/details/',DetailsHome),
    ('/details/studentdetails',StudentDetails),
    ],debug = True)
