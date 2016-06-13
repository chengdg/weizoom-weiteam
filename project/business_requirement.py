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
from business.project.b_requirement import BRequirement
from business.project.b_requirement_repository import BRequirementRepository
from business.project.b_project import BProject
from business.project.b_project_repository import BProjectRepository


FIELD_MAP = {
	'importance': 'importance'
}


class BusinessRequirement(resource.Resource):
	app = 'project'
	resource = 'business_requirement'

	@login_required
	def api_get(request):
		project_id = request.GET['project_id']
		requirement_id = request.GET['requirement_id']
		b_requirement = BRequirementRepository.get().get_requirement(project_id, requirement_id)
		
		response = create_response(200)
		comments = []
		for b_comment in b_requirement.comments:
			comments.append({
				"id": b_comment.id,
				"content": b_comment.content,
				"creater": {
					"name": b_comment.creater.name,
					"thumbnail": b_comment.creater.thumbnail
				},
				"createdAt": b_comment.created_at.strftime("%Y-%m-%d %H:%M"),
			})
		response.data = {
			"id": b_requirement.id,
			"importance": b_requirement.importance,
			"title": b_requirement.title,
			"content": b_requirement.content,
			"createdAt": b_requirement.created_at.strftime("%Y-%m-%d %H:%M"),
			"comments": comments,
			"creater": {
				"name": b_requirement.creater.name,
				"thumbnail": b_requirement.creater.thumbnail
			}
		}
		return response.get_response()
	
	@login_required
	def api_put(request):
		project_id = request.POST['project_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)
		b_project.add_business_requirement({
			"owner": request.user,
			"title": request.POST['title'],
			"importance": request.POST['importance'],
			"content": request.POST['content']
		})
		
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		requirement_id = request.POST['requirement_id']
		b_project = BProjectRepository.get().get_project_by_id(request.POST['project_id'])

		field = FIELD_MAP.get(request.POST['field'], None)
		value = request.POST['value']
		if not field:
			response = create_response(500)
			response.errMsg = u'不支持更新该属性'
		else:
			if not b_project.update_business_requirement(requirement_id, field, value):
				response = create_response(500)
				response.errMsg = u'更新属性失败'
			else:
				response = create_response(200)

		return response.get_response()

	@login_required
	def api_delete(request):
		project_id = request.POST['project_id']
		requirement_id = request.POST['requirement_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)
		b_project.delete_requirement(requirement_id)

		response = create_response(200)
		return response.get_response()