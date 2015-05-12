import webapp2

from google.appengine.ext import ndb
from main import Chrome,browser_key
from Intermediate import Student,student_key,eventData,Url,Student
from Meta import Meta,metaData_key
from Duration import DayDuration,duration_key

import datetime
import json

##class for generating DayDuration Manually
class Manual(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get("email")
        try:
            global start_date
            start_date = datetime.datetime.strptime("27/04/2015 00:00:00",'%d/%m/%Y %H:%M:%S')
            end_date = datetime.date.today()
            Duration = {}

            while(end_date > start_date.date()):
                date_str = datetime.datetime.strftime(start_date,"%d/%m/%Y %H:%M:%S")
                next_date = start_date+datetime.timedelta(days = 1)
                next_date_str = datetime.datetime.strftime(next_date,"%d/%m/%Y %H:%M:%S")

                chro = self.request.get('browser_name','chrome_data')
                qry = Chrome.query(ancestor = browser_key(chro))
                qry1 = qry.filter(Chrome.email == mail)
                qry2 = qry1.filter(Chrome.timeStamp >=date_str)
                qry3 = qry2.filter(Chrome.timeStamp <next_date_str)
                dataa = qry3.fetch()
                result_data = []
                for row in dataa:
                    result_data.append([row.urlLink,row.timeStamp])

                stu = self.request.get('student','student')
                qry = Student.query(ancestor = student_key(stu))
                qry1 = qry.filter(Student.email == mail)
                qry2 = qry1.filter(Student.uRl.eventdata.eventTime >=date_str)
                qry3 = qry2.filter(Student.uRl.eventdata.eventTime <next_date_str)
                dataa = qry3.fetch()
                for row in dataa:
                    result_data.append([row.uRl.url,row.uRl.eventdata.eventTime])
                data =  sorted(result_data,key = lambda x:x[1])
                global count
                count = 0
                global start
                start = "0"
                global end
                end = "0"
                global st
                global et
                global url
                global duration
                duration = 0
                for record in data:
                    if count == 0:
                        start = record[1]
                        st = datetime.datetime.strptime(record[1],'%d/%m/%Y %H:%M:%S')
                        url = record[0]
                        et = st
                        duration = et-st
                    elif count == len(data)-1:
                        end = record[1]
                        if(url != record[0]):
                            duration = duration+(et-st)
                        else:
                            et = datetime.datetime.strptime(record[1],'%d/%m/%Y %H:%M:%S')
                            duration = duration+(et-st)
                    else:
                        if(url != record[0]):
                            duration = duration+(et-st)
                            st = datetime.datetime.strptime(record[1],'%d/%m/%Y %H:%M:%S')
                            et = st
                            url = record[0]
                        else:
                            et = datetime.datetime.strptime(record[1],'%d/%m/%Y %H:%M:%S')
                    count = count +1
                Duration[datetime.datetime.strftime(start_date.date(),"%d/%m/%Y")] = [start,end,duration]
                start_date = start_date+datetime.timedelta(days = 1)
            for record in Duration:
                try:
                    du = self.request.get("duration","duration")
                    duration = DayDuration(parent = duration_key(du))
                    duration.email = mail
                    duration.date = record
                    duration.startTime = Duration[record][0]
                    duration.endTime = Duration[record][1]
                    duration.duration = str(Duration[record][2])
                    duration.put()
                except Exception,e:
                    self.response.write("inner exception: "+str(e))
            self.response.write('success')
        except Exception,e:
            self.response.write(str(e))

app = webapp2.WSGIApplication([
    ('/cron/insert',Manual),
    ],debug = True)
