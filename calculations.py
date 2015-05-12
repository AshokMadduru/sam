import webapp2
import jinja2
import os
import urllib
import datetime

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
    def get(self):
        mail = 'akella.keerthi@gmail.com'
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
            diffs = []
            tot_data = []
            mode = {}
            for row in data:
                if count == 0:
                    url = row.uRl.url
                    time = row.uRl.eventdata.eventTime
                    st = time
                    start = datetime.datetime.strptime(time,"%d/%m/%Y %H:%M:%S")
                    duration = start-start
                elif count == len(data)-1:
                    time = row.uRl.eventdata.eventTime
                    end = datetime.datetime.strptime(time,"%d/%m/%Y %H:%M:%S")
                    diff = start-end
                    if diff in mode:
                        mode[str(diff)] = mode[str(diff)]+diff
                    else:
                        mode[str(diff)] = diff
                    duration = duration+diff
                    diffs.append(str(diff))
                    tot_data.append([url,time,st,diff])
                else:
                    if url != row.uRl.url:
                        time = row.uRl.eventdata.eventTime
                        end = datetime.datetime.strptime(time,"%d/%m/%Y %H:%M:%S")
                        diff = start-end
                        if diff in mode:
                            mode[str(diff)] = mode[str(diff)]+diff
                        else:
                            mode[str(diff)] = diff
                        duration = duration+diff
                        diffs.append(str(diff))
                        tot_data.append([url,time,st,diff])
                        start = end
                        st = time
                        url = row.uRl.url
                count = count + 1
            # mean
            mean = duration/len(data)
            # median
            sorted_diffs = sorted(diffs)
            median = sorted_diffs[len(diffs)/2]
            # mode
            Mode = start-start
            for record in mode:
                if mode[record]>Mode:
                    Mode = mode[record]
            # send data to html as template values
            template_values = {'mean':mean, 'median':median,'mode':Mode}
            # render template
            template = JINJA_ENVIRONMENT.get_template('calculations.html')
            self.response.write(template.render(template_values))
        except Exception,e:
            self.response.write('Failed: '+str(e))
############################################################

## path specifier for math calculation
app = webapp2.WSGIApplication([
    ('/calc/calc',Maths),
    ],debug = True)
