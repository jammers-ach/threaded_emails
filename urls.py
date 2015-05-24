from django.conf.urls import patterns,include,url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.test, name='test'),
    url(r'^send_email$', views.send_template, name='send_email'),
    url(r'^i(?P<box_id>\d*)/$',views.all_mail,name='mailbox'),
    url(r'^i(?P<box_id>\d*)/check$',views.check_mail,name='check_mail'),
    url(r'^i(?P<box_id>\d*)/check_redirect$',views.check_mail,{'send_to':'/'},name='check_mail_redirect'),
    url(r'^m(?P<msg_id>\d*)/$',views.view_thread,name='view_thread'),
    url(r'^m(?P<msg_id>\d*)/full$',views.full_email,name='full_email'),
    url(r'^m(?P<msg_id>\d*)/delete$',views.delete_email,name='delete_email'),
    url(r'^fl(?P<msg_id>\d*)/$',views.view_flat,name='view_flat'),



    url(r'^templates/$',views.list_template,name='list_templates'),
    url(r'^templates/edit_template/(?P<obj_id>\d*)$',views.EditTemplateView.as_view(),name='edit_template'),
    url(r'^templates/edit_category/(?P<obj_id>\d*)$',views.EditCategoryView.as_view(),name='edit_category'),
    url(r'^templates/add_category$',views.AddCategoryView.as_view(),name='add_category'),
    url(r'^templates/add_template/(?P<obj_id>\d*)$',views.AddTemplateView.as_view(),name='add_template'),
)
