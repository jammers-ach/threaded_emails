from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse

from .models import MailBox, EmailMessage,EmailTemplate
from .forms import EmailForm
from .quick_imap import make_msg
from .templating import fill_in_template

from django.views.generic import View
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



class FillInTemplateView(View):
    '''Each page that wants to apply a template to an object(s) wants to do it over ajax
    this will allow you to create a view that will fill in the template for a set of objects

    Send your subject/body in 's' and 'b' and the ID of the template in 't' in get
    then define an mapping between (get_paramater:classes)when you subclass this view

    e.g.: FillInTemplateView.as_view(object_list={'u':User,'p':Problem})

    this will then call
    fill_template(request.GET['s'],request.GET['b'],[User.objects.get(request.GET['u'],.....] )

    '''
    object_list = {}

    def get(self,request):
        template = EmailTemplate.objects.get(id=request.GET['t'])
        objs = [ (o.objects.get(request.GET[k])) for o,k in self.object_list.iteritems() ]

        subject,body = fill_in_template(template.default_subject,objs),fill_in_template(template.text,objs)

        return JsonResponse({'s':subject,'b':body})

