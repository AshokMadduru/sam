import webapp2
from google.appengine.ext import ndb

import datetime
import jinja2
import os
import json

import cgi
import urllib

## Generating key for metadata
def metaData_key(meta_name = "meta"):
    return ndb.Key("Meta",meta_name)

## Model for metaData
class Meta(ndb.Model):
    chapter = ndb.StringProperty(indexed = True)
    moduleNo = ndb.IntegerProperty(indexed = True)
    url = ndb.StringProperty(indexed = True)
    title = ndb.StringProperty(indexed = False)
    moduleType = ndb.StringProperty(indexed = False)
    qtype = ndb.StringProperty(indexed = False)
    duration = ndb.StringProperty(indexed = False)

## class for storing metadata
class StoreMeta(webapp2.RequestHandler):
    def post(self):
        chap = self.request.get("chapter")
        module = self.request.get("moduleno")
        uRl = self.request.get("url")
        tiTle = self.request.get("title")
        tyPe = self.request.get("type")
        duRation = self.request.get("duration")
        quizType = self.request.get("qtype")
        if uRl is not None :
            try:
                data = Meta(chapter = chap, moduleNo = int(module),
                            url = uRl, title = tiTle,
                            moduleType = tyPe,
                            qtype = quizType, duration = duRation)
                data.put()
                self.response.write("success")
            except Exception, e:
                self.response.write(str(e))
        else:
            self.response.write("failed")

app = webapp2.WSGIApplication([
    ('/meta/insert',StoreMeta),
    ],debug = True)
