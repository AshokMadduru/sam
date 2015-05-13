"""
CSV.py file used for generating csv files for each date for all students
"""
##############################
## imports section
import webapp2
import datetime
import json

from google.appengine.ext import ndb
from main import Chrome,browser_key
from Intermediate import Student,student_key,eventData,Url,Student
##from Meta import Meta,metaData_key
##from Duration import DayDuration,duration_key
###############################

class CSV(webapp2.RequestHandler):
    """
    CSV class for retrieving data for a student for a given date.
    input: email and date from the user
    output: dictionary containing records for a given day.
    """
    def post(self):
        """
        post method will be called first whenver the CSV file invokes.
        It takes the email and date from the user as request.
        """

        email = self.request.get("email")
        date = self.request.get("date")
        
        # if email or date is None response with invalid date or email
        if email is not None or date is not None:
            #start date in datetime.datetime formate
            start_date = datetime.datetime.strptime(date,'%d/%m/%Y %H:%M:%S')
            # next date
            end_date = start_date+datetime.timedelta(days = 1)
            # next date in string formate
            end_date_str = datetime.datetime.strftime(end_date,
                                                      '%d/%m/%Y %H:%M:%S')
            try:
                # Get data from Chrome Table
                chro = self.request.get('browser_name','chrome_data')
                qry = Chrome.query(ancestor = browser_key(chro))
                qry1 = qry.filter(Chrome.email == email)
                qry2 = qry1.filter(Chrome.timeStamp >=date)
                qry3 = qry2.filter(Chrome.timeStamp <end_date_str)
                data = qry3.fetch()
                result_data = []
                # put this data in result_data list
                for row in data:
                    temp = {}
                    temp['eventype'] = row.eventType
                    temp['url'] = row.urlLink
                    temp['data'] = row.datas
                    temp['timeStamp'] = row.timeStamp
                    result_data.append(temp)
                # get data from Student table
                stu = self.request.get('student','student')
                qry = Student.query(ancestor = student_key(stu))
                qry1 = qry.filter(Student.email == email)
                qry2 = qry1.filter(Student.uRl.eventdata.eventTime >=date)
                qry3 = qry2.filter(Student.uRl.eventdata.eventTime <
                                   end_date_str)
                dataa = qry3.fetch()
                # Append this data result_data list
                for row in dataa:
                    temp = {}
                    temp['eventype'] = row.uRl.eventdata.eventtype
                    temp['url'] = row.uRl.url
                    temp['data'] = row.uRl.eventdata.eventData
                    temp['timeStamp'] = row.uRl.eventdata.eventTime
                    result_data.append(temp)
                # send the data as response in json format
                self.response.write(json.dumps({'data':result_data}))
            except Exception,e:
                self.response.write('error in querying: '+str(e))
        else:
            self.response.write('send valid email and date')

## Map the classes with urls
app = webapp2.WSGIApplication([
    ('/csv/',CSV),
    ],debug = True)
