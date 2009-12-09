import logging

from google.appengine.api import mail

def send_email(**kwds):
    logging.info('Sending email')
    mail.send_mail(**kwds)
