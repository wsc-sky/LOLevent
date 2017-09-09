from django.conf.urls import  include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
admin.autodiscover()

from main.views import *
from jp_test.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', user_home),
    url(r'^home/$', user_home),
    url(r'^home/(?P<page_num>\d+)/$', user_home),

    #sort
    url(r'^home/sort/(?P<sort_id>\d+)/$', user_home),


    url(r'^event_detial/(?P<e_id>\d+)/$', event_detial),

    url(r'^user/profile/(?P<user_id>\d+)/$', user_profile),

    #user_search and admin search

    url(r'^user/search/$', user_search),
    url(r'^user/date_search/$', date_range_search),
    url(r'^admin/search/$', admin_search),


    #comment 
    url(r'^comment/(?P<event_id>\d+)/(?P<u_name>\w+)/(?P<user_id>\d+)/$', comment),
    url(r'^comment/(?P<event_id>\d+)//None/$', comment),
    url(r'^comment/delete/(?P<event_id>\d+)/(?P<comment_id>\d+)/$', comment_delete),

    #like
    url(r'^like/(?P<event_id>\d+)/(?P<user_id>\d+)/(?P<user_name>\w+)/$', like),
    url(r'^like/(?P<event_id>\d+)/None/$', like),

    #home_like
    url(r'^like2/(?P<event_id>\d+)/(?P<user_id>\d+)/(?P<user_name>\w+)/$', home_like),
    url(r'^like2/(?P<event_id>\d+)/None//$', home_like),

    #paticipate
    url(r'^paticipate/(?P<event_id>\d+)/(?P<user_id>\d+)/(?P<user_name>\w+)/$', paticipate),   
    url(r'^paticipate/(?P<event_id>\d+)/None/$', paticipate),   
    
    #home_paticipate
    url(r'^paticipate2/(?P<event_id>\d+)/(?P<user_id>\d+)/(?P<user_name>\w+)/$', home_paticipate),   
    url(r'^paticipate2/(?P<event_id>\d+)/None/$', home_paticipate), 


    # Login, Logout and accounts
    url(r'^accounts/login/$', account_login),
    url(r'^accounts/login/(?P<event_id>\d+)/$', account_login),
    url(r'^accounts/logout/$', account_logout),
    url(r'^accounts/register/$', account_register),
    url(r'^accounts/activate/$', account_activate),
    url(r'^accounts/forgot/$', account_forgot),
    url(r'^accounts/reset/$', account_reset),



    # Control Panel
    url(r'^control/$', control),

    url(r'^control/insert/$', event_insert),
    #url(r'^control.insert/(?P<event_id>\d+)/$', insert_successful)
    url(r'^control/insert_s/$', event_s),
    url(r'^control/management/$', event_management),
    url(r'^control/edit/(?P<event_id>\d+)/$', event_edit),
    url(r'^delete/(?P<event_id>\d+)/$', event_delete),

    url(r'^control/edit/$', event_edit),





]
