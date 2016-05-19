# -*- coding: utf-8 -*-

from django.conf.urls import *

import views
import api_views
import debug_api_views
import statistics_views
import accounts_views
import accounts_api_views
import settings_views
import accounts_landing_views

urlpatterns = patterns('',
	
	#Sub account
	(r'sub_users/$', views.list_sub_accounts),
	(r'sub_user/create/$', views.create_sub_user),
	(r'sub_user/delete/$', views.delete_sub_user),

	#debug api url
	(r'logapi/log_api_error/$', debug_api_views.log_api_error),
	(r'js_error/log/$', debug_api_views.log_js_error),

	(r'api/weixin_mp_user_temp_message/create/$', api_views.create_weixin_mp_user_temp_message),
	(r'api/weixin_mp_user_temp_messages/get/$', api_views.get_weixin_mp_user_temp_messages),
	(r'api/sessionid/get/$', api_views.get_session_id),
	(r'api/social_account_token/get/$', api_views.get_social_account_token),

	(r'api/authorized_user_from_other_site/create/$', accounts_api_views.create_authorized_user_from_other_site),
	(r'api/authorized_user/create/$', accounts_api_views.create_authorized_user),
	(r'api/account_password/reset/$', accounts_api_views.reset_account_password),
	(r'api/inactive_account/create/$', accounts_api_views.create_inactive_account),

	(r'api/mpuser/emulate_bind/$', api_views.bind_mpuser),
	(r'api/binded_mpuser/delete/$', api_views.delete_binded_mpuser),
	(r'api/binded_mpuser/update/$', api_views.update_binded_mpuser),
	(r'api/bind_status/get/$', api_views.get_bind_status),
	(r'api/mpuser_access_token/create/$', api_views.create_mpuser_access_token),
	
	(r'upload_picture/$', views.upload_picture),
	(r'upload_icon/$', views.upload_icon),
	(r'upload_video/$', views.upload_video),
	(r'upload_richtexteditor_picture/$', views.upload_richtexteditor_picture),
	(r'upload_head_image/$', views.upload_head_image),

	(r'statistics/daily_new_weixin_user_trend/get/', statistics_views.get_new_weixin_user_daily_trend),
	# 邮件配置 zhaolei 2015-11-19
	# url(r'setting/notify/update/(\d+)/$', settings_views.update_email_status),

	#icon api url
	url(r'user_icons/get/$', api_views.get_user_icons),	

	#accounts urls
	(r'accounts/$', accounts_views.list_accounts),
	(r'created_user/delete/$', accounts_views.delete_account),
	(r'api/new_username/check/$', accounts_api_views.check_new_username),
	(r'api/user/create/$', accounts_api_views.create_new_user),
	(r'api/user/update/$', accounts_api_views.update_new_user),

	(r'api/user_by_agent/create/$', accounts_api_views.create_new_user_by_agent),
	(r'api/user_by_agent/delete/$', accounts_api_views.delete_user_by_agent),  #add by duhao 20151020
	
	#landing page urls
	# (r'index/$', accounts_landing_views.landing_index),
	(r'help_center/$', accounts_landing_views.help_center),
	(r'notice_list/$', accounts_landing_views.notice_list),
	(r'api/user_by_agent/update/$', accounts_api_views.update_user_by_agent),

)