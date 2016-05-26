# -*- coding: utf-8 -*-
import json
import time
import logging
from datetime import datetime, timedelta

from behave import *
import bdd_util
from django.contrib.auth import models as auth_models

@when(u"manager添加用户")
def step_impl(context):
	users = json.loads(context.text)
	for user in users:
		user['password'] = 'test'
		if not 'thumbnail' in user:
			user['thumbnail'] = '/static/img/default_user.jpg'
		response = context.client.put('/account/api/user/', user)
		bdd_util.assert_api_call_success(response)


@when(u"manager删除用户'{user_name}'")
def step_impl(context, user_name):
	user = auth_models.User.objects.get(username=user_name)

	response = context.client.delete('/account/api/user/', {'id': user.id})
	bdd_util.assert_api_call_success(response)


@then(u"manager能获得用户列表")
def step_impl(context):
	expected = json.loads(context.text)

	response = context.client.get('/account/users/')
	users = response.context['frontend_data'].get('users')
	filter_username_set = set(['zhouxun', 'yangmi', 'leijun', 'yaochen'])
	actual = [user for user in users if not user['name'] in filter_username_set]
	for user in actual:
		user['real_name'] = user['realName']
	
	bdd_util.assert_list(expected, actual)