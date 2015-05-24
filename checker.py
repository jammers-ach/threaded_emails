'''Checks emails'''
from models import MailBox,EmailMessage
import django.dispatch
import logging
new_email = django.dispatch.Signal(providing_args=["email"])

def check_all_mailboxes():
    for mb in MailBox.objects.all():
        check_box(mb)

def check_box(mb):
    emails = mb.check_new_mail()
    print '[%s] %d new messages' % (mb,len(emails))
    new_emails = 0
    emails = mb.download_emails(emails)
    for email in emails:
        try:
            e = EmailMessage.from_email(email,mb)
        except Exception,exp:
            logging.exception(exp)
            e = None

        #Todo, check if message exists before sending signal..
        if(e != None):
            new_emails += 1
            new_email.send(sender=e.__class__,email=e)
            e.log_creation(None,'created through email check')
    return new_emails

