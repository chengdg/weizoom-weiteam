# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from behave import *
from features import bdd_util

from project.models import *


@when(u"{user}添加Project")
def step_impl(context, user):
	projects = json.loads(context.text)
	for project in projects:
		response = context.client.put('/project/api/project/', project)
		bdd_util.assert_api_call_success(response)


@when(u'{user}更新Project"{project_name}"')
def step_impl(context, user, project_name):
	project = bdd_util.get_project(context.client.user, project_name)

	project_data = json.loads(context.text)
	project_data['id'] = project.id

	url = '/project/api/project/'
	response = context.client.post(url, project_data)
	bdd_util.assert_api_call_success(response)


@when(u'{user}删除Project"{project_name}"')
def step_impl(context, user, project_name):
	project = bdd_util.get_project(context.client.user, project_name)

	project_data = {
		'id': project.id
	}

	url = '/project/api/project/'
	response = context.client.delete(url, project_data)
	bdd_util.assert_api_call_success(response)


@then(u'{user}能获得Project"{project_name}"')
def step_impl(context, user, project_name):
	project = bdd_util.get_project(context.client.user, project_name)

	url = '/project/api/project/?id=%d' % project.id
	response = context.client.get(url)
	actual = json.loads(response.content)['data']

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)


@then(u"{user}能获得Project列表")
def step_impl(context, user):
	response = context.client.get('/project/projects/')
	actual = response.context['frontend_data'].get('projects')

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)


@when(u"{user}访问项目'{project_name}'")
def step_impl(context, user, project_name):
	context.project = bdd_util.get_project(context.client.user, project_name)

@when(u"{user}访问项目看板")
def step_impl(context, user):
	context.project = bdd_util.get_project(context.client.user, u'看板')


@when(u"{user}设置'{project_user_name}'为项目'{project_name}'的管理员")
def step_impl(context, user, project_user_name, project_name):
	project = bdd_util.get_project(context.client.user, project_name)
	project_user_id = bdd_util.get_user_id_for(project_user_name)

	data = {
		'project_id': project.id,
		'user_id': project_user_id,
		'set_to_manager': 'true'
	}

	url = '/project/api/project_manager/set/'
	response = context.client.post(url, data)
	bdd_util.assert_api_call_success(response)


@when(u"{user}取消'{project_user_name}'作为项目'{project_name}'的管理员")
def step_impl(context, user, project_user_name, project_name):
	project = bdd_util.get_project(context.client.user, project_name)
	project_user_id = bdd_util.get_user_id_for(project_user_name)

	data = {
		'project_id': project.id,
		'user_id': project_user_id,
		'set_to_manager': 'false'
	}

	url = '/project/api/project_manager/set/'
	response = context.client.post(url, data)
	bdd_util.assert_api_call_success(response)


@then(u"{user}'{is_manager}'项目'{project_name}'的管理员")
def step_impl(context, user, is_manager, project_name):
	project = bdd_util.get_project(context.client.user, project_name)
	response = context.client.get('/project/users/?project_id=%d' % project.id)
	expected = True if is_manager == u'是' else False
	actual = response.context['request'].user.is_manager
	context.tc.assertEquals(expected, actual)


@then(u"{user}获得失败提示'{error_msg}'")
def step_impl(context, user, error_msg):
	response = context.last_response
	bdd_util.assert_api_call_failed(response, error_msg)
