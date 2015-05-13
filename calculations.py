## Contains Classes: Math
## Math: calculates the mean, mode and median of all students
##      for one day


import webapp2
import jinja2
import os
import urllib
import datetime
import json

from google.appengine.ext import ndb
from Intermediate import student_key,Url,eventData,Student

# Setting up the Jinja environment to include html pages as templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

############################################################
## class for Calculating Mean , Mode and Median for one day of all students
class Maths(webapp2.RequestHandler):
    def post(self):
        mail = self.request.get('email')
        #start date
        start = '05/05/2015 00:00:00'
        # end date
        end = '06/05/2015 00:00:00'
        try:
            # get data from student table
            stu = self.request.get('student','student')
            qry = Student.query(ancestor = student_key(stu))
            qry1 = qry.filter(Student.email == mail)
            qry2 = qry1.filter(Student.uRl.eventdata.eventTime >=start)
            qry3 = qry2.filter(Student.uRl.eventdata.eventTime < end)
            qry = qry3.order(-(Student.uRl.eventdata.eventTime))
            data = qry.fetch()

            # find the diff time between successive differrent urls
            count = 0
            global start
            global st
            global url
            global end
            global duration
            curr_time = datetime.datetime.now()
            duration = (curr_time - curr_time).seconds
            diffs = []
            tot_data = []
            mode = {}
            for row in data:
                if count == 0:
                    url = row.uRl.url
                    time = row.uRl.eventdata.eventTime
                    st = time
                    start = datetime.datetime.strptime(time,"%d/%m/%Y %H:%M:%S")
                elif count == len(data)-1:
                    time = row.uRl.eventdata.eventTime
                    end = datetime.datetime.strptime(time,"%d/%m/%Y %H:%M:%S")
                    diff = (start-end).seconds
                    if str(diff) in mode:
                        mode[str(diff)] = mode[str(diff)]+1
                    else:
                        mode[str(diff)] = 1
                    duration = duration+diff
                    diffs.append(str(diff))
                    tot_data.append([url,time,st,diff])
                else:
                    if url != row.uRl.url:
                        time = row.uRl.eventdata.eventTime
                        end = datetime.datetime.strptime(time,"%d/%m/%Y %H:%M:%S")
                        diff = (start-end).seconds
                        if str(diff) in mode:
                            mode[str(diff)] = mode[str(diff)]+1
                        else:
                            mode[str(diff)] = 1
                        duration = duration+diff
                        diffs.append(str(diff))
                        tot_data.append([url,time,st,diff])
                        start = end
                        st = time
                        url = row.uRl.url
                count = count + 1
            # mean
            global mean
            if len(data) == 0:
                mean = 0
            else:
                mean = duration/len(tot_data)
            # median
            global median
            sorted_diffs = sorted(diffs)
            if len(diffs) == 0:
                median = 0
            else:
                median = sorted_diffs[len(diffs)/2]
            # mode
            global Mode
            if len(data) == 0:
                Mode = "0"
            else:
                temp = (curr_time-curr_time).seconds
                for record in mode:
                    if mode[record]>temp:
                        Mode = record
            # send data to html as template values
            #template_values = {'mean':mean, 'median':median,'mode':Mode}
            # render template
            #template = JINJA_ENVIRONMENT.get_template('calculations.html')
            #self.response.write(template.render(template_values))
            values = [mean,median,Mode]
            self.response.write(json.dumps({'values':[str(mean),str(median),str(Mode)]}))
        except Exception,e:
            self.response.write('Failed: '+str(e))
############################################################

## path specifier for math calculation
app = webapp2.WSGIApplication([
    ('/calc/calc',Maths),
    ],debug = True)
