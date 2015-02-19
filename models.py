from django.db import models
from modelwithlog.models import ModelWithLog
# Create your models here.
from quick_imap import ImapConnection
import datetime
import smtplib
#http://www.jwz.org/doc/threading.html
import email
import time

class MailBox(ModelWithLog):
    mailbox_choices = ((1,'IMAP'),(2,'POP'))

    mailbox_type = models.IntegerField(default=1,choices=mailbox_choices)
    server = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    last_check_date = models.DateTimeField(blank=True,null=True)

    smtp_address = models.CharField(max_length=100)
    from_addr = models.CharField(max_length=100)

    #To add:
    #check_type - what do we read only, or read and clear the read flag
    #check_frequency - how often do we read (max 1 every 5 minutes)
    #autocheck - automatically check this or not (requires cronscripts!!)
    #last_check_date - timestamp for last check date
    #smtp_user
    #smtp_password

    def __unicode__(self):
        return '%s@%s' % (self.account,self.server)


    def check_new_mail(self):
        '''Checks the mailbox for new messages'''
        self.conn = ImapConnection(self.server,self.account,self.password)
        self.conn.login()
        emails = self.conn.get_unread_emails()

        if(len(emails) > 0):
            #RUROH NEW MAILS
            self.log_change(None,'%d new message at check' % len(emails))
        self.last_check_date = datetime.datetime.now()
        self.save()

        return emails

    def download_emails(self,email_list):
        '''Downloads the emails from the server'''
        return self.conn.get_emails(email_list)


    def logout(self):
        self.conn.logout()

    def send_mail(self,msg,to):
        '''sends a MIMEText message (msg)'''
        print 'Creating STMP'
        s = smtplib.SMTP(self.smtp_address)
        s.ehlo()
        s.starttls()
        msg['Message-Id'] = email.utils.make_msgid('mbox-%d' % self.pk)
        print 'Message id:',msg['Message-Id']
        s.login(self.account,self.password)
        msg['from'] = self.from_addr

        s.sendmail(self.from_addr, to, msg.as_string())
        s.quit()


        EmailMessage.from_email(msg,self)

    def root_emails(self):
        q = EmailMessage.objects.filter(mailbox=self).filter(reply_to__isnull=True).order_by('-time_sent')
        return q

class EmailMessage(ModelWithLog):
    '''Holds an email message'''
    to_addr = models.EmailField()
    from_addr = models.EmailField()
    mailbox = models.ForeignKey(MailBox)
    subject = models.TextField()
    body = models.TextField(blank=True,null=True)

    message_id = models.CharField(max_length =200,unique=True) #200, whatever or 5 who knows?

    reply_to = models.CharField(max_length =200,blank=True,null=True)
    parent = models.ForeignKey('EmailMessage',blank=True,null=True)
    num_children = models.IntegerField(default=0)

    time_recived = models.DateTimeField()
    time_sent = models.DateTimeField()
    read = models.BooleanField(default=False)

    def children(self):
        return EmailMessage.objects.filter(parent=self)


    def children_date(self):

        max_child = [ c.children_date() for c in self.children().order_by('-time_recived')]

        if(max_child == []):
            return self
        else:
            return max_child[0]



    def last_child(self):
        ''' finds the deepest child in the thread'''
        return self.children_date()



    def log_child(self):
        if(self.parent):
            self.parent.log_child()
        else:
            self.num_children += 1
            self.save()

    def thread_size(self):
        return self.num_children + 1

    def __unicode__(self):
        return self.message_id

    @classmethod
    def from_email(klass,eml,mbox):
        '''Creates an email from an email.message.Message object'''

        if(klass.objects.filter(message_id=eml['message-id']).exists()):
            print '[%s] message exists %s ' % (mbox,eml['message-id'])
            return


        print 'In reply to: %s' % eml['In-Reply-To']
        e = klass()
        e.message_id = eml['message-id']
        e.to_addr = eml['to']
        if(eml['from'] != None):
            e.from_addr = eml['from']
        else:
            e.from_addr = mbox.from_addr
        e.mailbox = mbox
        e.subject = eml['subject']
        e.time_recived = datetime.datetime.now()

        if('Date' in eml):
            e.time_sent = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(eml['Date'])))
        else:
            e.time_sent = datetime.datetime.now()

        #If we have a reply, find the parent and link ourselves and increment
        e.reply_to = eml['In-Reply-To']
        if(e.reply_to):
            parent = klass.objects.filter(message_id=e.reply_to)
            if(parent.exists()):
                parent = parent[0]
                e.parent = parent
                parent.log_child()


        p = ''
        if eml.is_multipart():
            for payload in eml.get_payload():
                p += payload.get_payload()
        else:
            print type(eml.get_payload())
            p += eml.get_payload()
        e.body = p

        e.save()

        #lets see if there are any emails that we should be the parents of?
        q = klass.objects.filter(parent__isnull=True,reply_to=e.message_id)
        if(q.exists()):
            q.update(parent=e)
            e.num_children = q.count()

        return e

