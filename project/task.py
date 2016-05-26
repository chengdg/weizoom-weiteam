# -*- coding: utf-8 -*-
import json
import time
import base64

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import nav
import models
from resource import models as resource_models
from util import string_util
from business.project.b_task import BTask
from business.project.b_task_repository import BTaskRepository

FIELD_MAP = {
	'importance': 'importance',
	'storyPoint': 'story_point'
}

class Task(resource.Resource):
	app = 'project'
	resource = 'task'
	
	@login_required
	def api_get(request):
		b_task = BTaskRepository.get().get_task(request.GET['id'])

		data = {
			'id': b_task.id,
			'title': b_task.title,
			'type': b_task.type,
			'importance': b_task.importance,
			'storyPoint': b_task.story_point,
			'content': b_task.content
		}

		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_post(request):
		b_task = BTaskRepository.get().get_task(request.POST['id'])

		field = FIELD_MAP.get(request.POST['field'], None)
		value = request.POST['value']
		if not field:
			response = create_response(500)
			response.errMsg = u'不支持更新该属性'
		else:
			if not b_task.update(field, value):
				response = create_response(500)
				response.errMsg = u'更新属性失败'
			else:
				response = create_response(200)

		return response.get_response()

