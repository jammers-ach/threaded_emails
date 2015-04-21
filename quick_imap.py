import imaplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename
import datetime

class ImapConnection(object):
    '''Connects to an IMAP server
    gets emails'''

    def __init__(self,server,username,password):
        self.server = server
        self.username = username
        self.password = password

    def get_emails(self,email_ids):
        '''Gets the content of each email from a list of ids'''
        data = []
        for e_id in email_ids:
            print 'email_id',e_id
            _, response = self.imap_server.fetch(e_id, '(RFC822)')
            msg = email.message_from_string(response[0][1])
            data.append(msg)
        return data

    def get_subjects(self,email_ids):
        '''Gets the subjects from each email'''
        subjects = []
        for e_id in email_ids:
            _, response = self.imap_server.fetch(e_id, '(body[header.fields (subject)])')
            print response
            subjects.append( response[0][1][9:] )
        return subjects

    def login(self):
        '''logs into the imap server'''
        imap_server = imaplib.IMAP4_SSL(self.server)
        imap_server.login(self.username, self.password)
        self.imap_server = imap_server

    def select(self,what):
        self.imap_server.select(what)

    def _search(self,where,what):
        return self.imap_server.search(where,what)

    def get_unread_emails(self,clear_read=False,date=None):
        self.imap_server.select(readonly=1) # Select inbox or default namespace

        if(date == None):
            date = datetime.date.today() #- datetime.timedelta(days=1)
        dstring = date.strftime('%d-%b-%Y')
        print dstring
        retcode,messages = self.imap_server.search(None, '(SINCE "%s")' % dstring)
        #if(clear_read and len(messages[0]) > 0):
            #self.imap_server.store(messages[0].replace(' ',','),'+FLAGS','\Seen')

        return messages[0].split()

    def get_all_emails(self):
        return self._search(None,'All')[1][0].split()

    def logout(self):
        self.imap_server.logout()


import cStringIO as StringIO


def make_msg(subject,body,toaddr,fromaddr,reply_to=None,files=[]):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    if(reply_to):
        msg['In-Reply-To'] = reply_to

    msg.attach(MIMEText(body, 'plain',_charset='utf-8'))

    msg['Content-Type'] = 'text/plain;charset=utf-8;format="flowed"'

    for f in files or []:
        if(isinstance(f, basestring)):
            fil = open(f, "rb")
            fname = basename(f)
        else:
            fil = open(f[0],"rb")
            fname = f[1]
        print 'attaching %s' % fname

        attachment = MIMEApplication(fil.read())
        attachment.add_header("Content-Disposition", "attachment", filename=fname)
        msg.attach(attachment)
        #msg.attach(MIMEApplication(
            #fil.read(),
            #Content_Disposition='attachment; filename="%s"' % basename(f)
        #))



    return msg
