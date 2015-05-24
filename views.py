from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse

from .models import MailBox, EmailMessage,EmailTemplate,EmailTemplateCategory
from .forms import EmailForm,EmailTemplateCategoryForm,EmailTemplateForm
from .quick_imap import make_msg
from .templating import populate_email
from django.contrib import messages
from django.http import Http404

from django.views.generic import View
from django.contrib.auth.decorators import login_required
from checker import check_box
# Create your views here.

from bootstrap_form.views import *

from django.utils.translation import ugettext as _
def test(request):
    mailboxes = MailBox.objects.all()
    return render(request,'threaded_emails/console.html',{'boxes':mailboxes});


def all_mail(request,box_id):
    box = MailBox.objects.get(id=box_id)
    return render(request,'threaded_emails/inbox.html',{'box':box})

def check_mail(request,box_id,send_to=None):
    box = MailBox.objects.get(id=box_id)
    #Check mail
    count = check_box(box)
    messages.success(request,_('%d new messages') % count)
    #reverse
    if not send_to:
        send_to = reverse('emails:mailbox',kwargs={'box_id':box_id})
    return redirect(send_to)

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


def send_template(request):
    '''Sends an email from the template form'''

    if(request.method == 'POST'):
        mbox = MailBox.objects.all()[0] #TODO make pick the mailbox more nicely
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        to = request.POST.get('to')

        msg = make_msg(subject,body,to,mbox.from_addr)
        mbox.send_mail(msg,to)
        messages.success(request,'Email sent' )
        return redirect(request.POST.get('redirect'))
    else:
        raise Http404('method not post')


def full_email(request,msg_id):
    msg = EmailMessage.objects.get(id=msg_id)

    if('body' in request.GET):
        body = request.GET['body']
        to = request.GET['to']
        mbox = MailBox.objects.all()[0] #TODO make pick the mailbox more nicely

        subject = msg.get_reply_subject()
        msg = make_msg(subject,body,to,mbox.from_addr,reply_to=msg.message_id)
        mbox.send_mail(msg,to)

    return render(request,'threaded_emails/includes/msg_body.html',{'msg':msg})

@login_required
def delete_email(request,msg_id):
    msg = EmailMessage.objects.get(id=msg_id)
    msg.delete()

    messages.success(request,'Email deleted')

    return redirect(request.GET.get('r','/'))

def view_flat(request,msg_id):
    msg = EmailMessage.objects.get(id=msg_id)
    email = EmailForm(initial={'to':msg.from_addr,'email_subject':'Re: ' + msg.subject})

    if(request.method=='POST'):
        email2 = EmailForm(request.POST)
        if(email2.is_valid()):
            to = email2.cleaned_data['to']
            body = email2.cleaned_data['email_text']
            subject = email2.cleaned_data['email_subject']
            mime_msg = make_msg(subject,body,to,None,msg.message_id)
            #add reply to flag
            msg.mailbox.send_mail(mime_msg,to)
        else:
            pass

    return render(request,'threaded_emails/flat_email.html',{'msg':msg,'email_form':email})




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
        objs = [ (o.objects.get(id=request.GET[k])) for k,o in self.object_list.iteritems() ]
        print objs

        subject,body = populate_email(template,objs)

        return JsonResponse({'s':subject,'b':body})



def list_template(request):
    categories = EmailTemplateCategory.objects.all().order_by('category_name')

    settings = {'categories':categories}

    return render(request,'threaded_emails/template_list.html',settings)


class AddCategoryView(NewObjView):
    obj_klass = EmailTemplateCategory
    form_klass =EmailTemplateCategoryForm
    redirect_page = 'emails:list_templates'


class EditCategoryView(EditObjView):
    obj_klass = EmailTemplateCategory
    form_klass =EmailTemplateCategoryForm
    redirect_page = 'emails:list_templates'

class AddTemplateView(NewObjView):
    obj_klass = EmailTemplate
    form_klass = EmailTemplateForm
    redirect_page = 'emails:list_templates'

    def get(self,request,obj_id):
        c = EmailTemplateCategory.objects.get(id=obj_id)
        form = self.form_klass(initial={'template_category':c})
        settings = {'f':form}
        settings.update(self.get_extra_settings())
        settings.update(self._settings_ovr)
        if('ajax' in request.GET and request.GET['ajax'] == 'true'):
            return render(request,self.ajax_template,settings)
        else:
            return render(request,self.template,settings)


    def post(self,request,obj_id):
        return super(AddTemplateView,self).post(request)

class EditTemplateView(EditObjView):
    obj_klass = EmailTemplate
    form_klass = EmailTemplateForm
    redirect_page = 'emails:list_templates'
    template = 'threaded_emails/edit_template.html'


    def get_extra_settings(self):
        '''Extra settings common to every view'''
        if(self.obj_name == None):
            self.obj_name = self.obj_klass.__name__

        return {'obj_name':self.obj_name,
                'template_objs':[],
                }



def get_codes_for_obj(request):
    pass
