from django.conf.urls import patterns,include,url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.test, name='test'),
    url(r'^i(?P<box_id>\d*)/$',views.all_mail,name='mailbox'),
    url(r'^i(?P<box_id>\d*)/check$',views.check_mail,name='check_mail'),
    url(r'^m(?P<msg_id>\d*)/$',views.view_thread,name='view_thread'),
    url(r'^m(?P<msg_id>\d*)/full$',views.full_email,name='full_email'),
)
