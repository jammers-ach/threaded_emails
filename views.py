from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from .models import MailBox, EmailMessage
from .forms import EmailForm
from .quick_imap import make_msg

from django.contrib.auth.decorators import login_required
from checker import check_box
# Create your views here.


def test(request):
    mailboxes = MailBox.objects.all()
    return render(request,'threaded_emails/console.html',{'boxes':mailboxes});


def all_mail(request,box_id):
    box = MailBox.objects.get(id=box_id)
    return render(request,'threaded_emails/inbox.html',{'box':box})

def check_mail(request,box_id):
    box = MailBox.objects.get(id=box_id)
    #Check mail
    check_box(box)
    #reverse
    return redirect(reverse('emails:mailbox',kwargs={'box_id':box_id}))

def view_thread(request,msg_id):
    msg = EmailMessage.objects.get(id=msg_id)

    #let's find the last message in the thread
    last_msg = msg.children_date()

    #reply to the person we heard from last, unles it's ourselves
    if(last_msg.from_addr.find(msg.mailbox.from_addr) > -1):
        from_addr = last_msg.to_addr
    else:
        from_addr = last_msg.from_addr



    if(request.method=='POST'):

        email2 = EmailForm(request.POST)
        if(email2.is_valid()):
            subject = 're: ' + last_msg.subject
            to = email2.cleaned_data['to']
            body = email2.cleaned_data['email_text']
            mime_msg = make_msg(subject,body,to,None,last_msg.message_id)
            #add reply to flag
            msg.mailbox.send_mail(mime_msg,to)
        else:
            pass
        #add notification


    email = EmailForm(initial={'to':from_addr})

    return render(request,'threaded_emails/message.html',{'msg':msg,'email_form':email,'last_msg':last_msg})


def full_email(request,msg_id):
    msg = EmailMessage.objects.get(id=msg_id)
    return HttpResponse(msg.body)

