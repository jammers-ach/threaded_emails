import imaplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

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

    def get_unread_emails(self):
        self.imap_server.select(readonly=1) # Select inbox or default namespace
        retcode,messages = self.imap_server.search(None, '(UNSEEN)')
        return messages[0].split()

    def get_all_emails(self):
        return self._search(None,'All')[1][0].split()

    def logout(self):
        self.imap_server.logout()




def make_msg(subject,body,toaddr,fromaddr,reply_to=None):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    if(reply_to):
        msg['In-Reply-To'] = reply_to

    msg.attach(MIMEText(body, 'plain'))
    return msg
