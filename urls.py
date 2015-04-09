from django.conf.urls import patterns,include,url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.test, name='test'),
    url(r'^send_email$', views.send_template, name='send_email'),
    url(r'^i(?P<box_id>\d*)/$',views.all_mail,name='mailbox'),
    url(r'^i(?P<box_id>\d*)/check$',views.check_mail,name='check_mail'),
    url(r'^m(?P<msg_id>\d*)/$',views.view_thread,name='view_thread'),
    url(r'^m(?P<msg_id>\d*)/full$',views.full_email,name='full_email'),
    url(r'^m(?P<msg_id>\d*)/delete$',views.delete_email,name='delete_email'),
    url(r'^fl(?P<msg_id>\d*)/$',views.view_flat,name='view_flat'),
)
