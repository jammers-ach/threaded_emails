import os
from django.conf import settings
from django.db import models
from modelwithlog.models import ModelWithLog
# Create your models here.
from quick_imap import ImapConnection
import datetime
import smtplib
#http://www.jwz.org/doc/threading.html
import email
import time
import re
from email.header import decode_header


def decode_string(e):
    if(e.startswith('=?')):
        print 'unicode header'
        h = decode_header(e)
        return unicode(*h[0])
    else:
        return unicode(e)

def strip_email(s):
    s = re.sub(r'.*<','',s)
    s = re.sub(r'>.*','',s)
    return s


class MailBox(ModelWithLog):
    mailbox_choices = ((1,'IMAP'),(2,'POP'))

    mailbox_type = models.IntegerField(default=1,choices=mailbox_choices)
    server = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    last_check_date = models.DateTimeField(blank=True,null=True)

    smtp_address = models.CharField(max_length=100)
    smtp_port = models.IntegerField(default=465)
    from_addr = models.CharField(max_length=100)


    clear_on_read = models.BooleanField(default=False)

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
        emails = self.conn.get_unread_emails(clear_read=self.clear_on_read)

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
        s = smtplib.SMTP(self.smtp_address,self.smtp_port)
        print 'ehlo'
        s.ehlo()
        print 'start ttls'
        s.starttls()
        msg['Message-Id'] = email.utils.make_msgid('mbox-%d' % self.pk)
        print 'Message id:',msg['Message-Id']
        s.login(str(self.account),str(self.password))
        s.ehlo()
        msg['from'] = self.from_addr

        s.sendmail(self.from_addr, to, msg.as_string())
        s.quit()


        e = EmailMessage.from_email(msg,self)
        from checker import new_email
        new_email.send(sender=e.__class__,email=e)

        return e


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
    body_html = models.TextField(blank=True,null=True)

    message_id = models.CharField(max_length =200,unique=True) #200, whatever or 5 who knows?

    reply_to = models.CharField(max_length =200,blank=True,null=True)
    parent = models.ForeignKey('EmailMessage',blank=True,null=True)
    num_children = models.IntegerField(default=0)

    time_recived = models.DateTimeField()
    time_sent = models.DateTimeField()
    read = models.BooleanField(default=False)


    def get_reply_subject(self):
        if(self.subject.lower().startswith('re:')):
           return self.subject
        else:
           return 're: ' + self.subject


    def get_root_email(self):
        '''Goes back up the tree to find the root of this conversation'''
        if(self.parent):
            return self.parent.get_root_email()
        else:
            return None



    def get_thread(self,thread=[]):
        '''finds all the emails in this thread'''

        thread.append(self)
        if(self.parent):
            return self.parent.get_thread(thread)

        else:
            return thread

    def stripped_to(self):
        return strip_email(self.to_addr)

    def stripped_from(self):
        return strip_email(self.from_addr)

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

    def hasattachments(self):
        return self.attachment_set.exists()


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
        e.message_id = unicode(eml['message-id'])
        e.to_addr = decode_string(eml['to'])
        if(eml['from'] != None):
            e.from_addr = decode_string(eml['from'])
        else:
            e.from_addr = mbox.from_addr
        e.mailbox = mbox
        e.subject = decode_string(eml['subject'])



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



        e.save()
        e.parse_body(eml) #need to save before we parse body because ATTACHMENTS
        e.save()

        #lets see if there are any emails that we should be the parents of?
        q = klass.objects.filter(parent__isnull=True,reply_to=e.message_id)
        if(q.exists()):
            q.update(parent=e)
            e.num_children = q.count()

        return e


    def parse_body(self,eml):
        ''' Parses an email body and sotres the body and html into the two parts'''
        self.body = u''
        self.body_html = u''
        if eml.is_multipart():
            for payload in eml.get_payload():
                self.handle_payload(payload)
        else:
            payload = eml.get_payload()
            self.handle_payload(payload)


    def handle_payload(self,payload):
        ''' Figures out which part of an email this should go'''
        #If we're text attach us to the messages
        if(isinstance(payload,basestring) ):
            self.body += payload
            return
        if(payload.get_content_maintype() == 'text'):
            if(payload.get_content_subtype() == 'plain'):
                self.body += decode_payload(payload)
            elif(payload.get_content_subtype() == 'html'):
                self.body_html += decode_payload(payload)
            else:
                Attachment.from_payload(payload,self).save()

        #If it's a multipart, recurse
        elif(payload.get_content_maintype() == 'multipart'):
            for payload in payload.get_payload():
                self.handle_payload(payload)
        #otherwise it's a file
        else:
            if(payload.get_filename(None) != None):
                #Save the file as an attachment
                Attachment.from_payload(payload,self).save()
            else:
                print 'Unrecognised payload',payload.get_content_type()


def decode_payload(payload):
    p = payload.get_payload(decode=True)
    try:
        return unicode(p)
    except UnicodeDecodeError,e:
        return p.decode(payload.get_charsets()[0])

class EmailTemplateCategory(ModelWithLog):
    '''A helpful way of organising email templates'''
    category_name = models.CharField(max_length=300)


    def __unicode__(self):
        return self.category_name

class EmailTemplate(ModelWithLog):
    '''An email with placeholders that are replaced later'''
    template_name = models.CharField(max_length=300)
    template_category = models.ForeignKey('EmailTemplateCategory')
    default_subject=  models.CharField(max_length=300)
    text = models.TextField()

    def __unicode__(self):
        return self.template_name




media_root = getattr(settings, "MEDIA_ROOT", "media")
media_url = getattr(settings, "MEDIA_URL", "media")

class Attachment(ModelWithLog):
    email = models.ForeignKey('EmailMessage')
    filepath = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    default_path = os.path.join(media_root,'uploads','emails')
    default_url = os.path.join(media_url,'uploads','emails')

    def __unicode__(self):
        return self.filename


    @classmethod
    def from_payload(klass,payload,email):
        '''creates a new attachment from an email payload '''
        #Create clsas, set our filename
        a = klass()
        a.email = email

        name = decode_string(payload.get_filename())
        a.filename = name


        test_dir = os.path.join(klass.default_path)
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)

        filepath = os.path.join(test_dir,name)
        print filepath


        #Figure out the filepath to store this attachment
        f = open(filepath, 'wb')
        f.write(payload.get_payload(decode=True))
        f.close()

        a.url  = os.path.join(klass.default_url,name)


        return a

