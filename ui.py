import os
import logging

from google.appengine.ext import deferred
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import emailqueuer

def make20khtmlchunk():
    html = '<html><body>'
    for x in xrange(20000):  # make a >20k html content part to make sure that works
        html += 'b'
    html += '</body></html>'
    return html

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'ui.html')
        self.response.out.write(template.render(path, locals()))
    def post(self):
        sender = self.request.get('sender')
        to = self.request.get('to')
        reply_to = self.request.get('reply_to')
        subject = self.request.get('subject')
        body = self.request.get('body')
        html = make20khtmlchunk()
            
        logging.info(locals())
        mailargs = locals()
        
        del mailargs['self']
        deferred.defer(emailqueuer.send_email, **mailargs)
        print 'Content-Type: text/plain'
        print ''
        print 'Queued.'

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
