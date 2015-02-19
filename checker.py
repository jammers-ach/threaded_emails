'''Checks emails'''
from models import MailBox,EmailMessage
import django.dispatch

new_email = django.dispatch.Signal(providing_args=["email"])

def check_all_mailboxes():
    for mb in MailBox.objects.all():
        check_box(mb)

def check_box(mb):
    emails = mb.check_new_mail()
    print '[%s] %d new messages' % (mb,len(emails))
    emails = mb.download_emails(emails)
    for email in emails:
        e = EmailMessage.from_email(email,mb)
        #Todo, check if message exists before sending signal..
        new_email.send(sender=e.__class__,email=e)
        if(e != None):
            e.log_creation(None,'created through email check')

