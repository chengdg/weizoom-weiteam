# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from core.restful_url import restful_url
from account import views as account_view


# from admin.sites import site
# site = admin_sites.AdminSite()

#import admin as loc_admin
#from weixin import sinulator_views as sinulator_views

urlpatterns = patterns('',
	url(r'^$', account_view.index),
	url(r'^project/', restful_url('project')),
	url(r'^account/', restful_url('account')),
	url(r'^resource/', restful_url('resource')),
)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'account.views.show_error_page'
handler500 = 'account.views.show_error_page'
