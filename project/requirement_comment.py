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
from business.project.b_requirement_repository import BRequirementRepository


class RequirementComment(resource.Resource):
	app = 'project'
	resource = 'requirement_comment'
	
	@login_required
	def api_put(request):
		project_id = request.POST['project_id']
		requirement_id = request.POST['requirement_id']
		content = request.POST['content']
		b_requirement = BRequirementRepository.get().get_requirement(project_id, requirement_id)
		comment = b_requirement.add_comment(request.user, content)
		
		data = {
			"id": comment.id,
			"creater": {
				"name": comment.creater.name,
				"thumbnail": comment.creater.thumbnail
			},
			"content": comment.content,
			"createdAt": comment.created_at.strftime("%Y-%m-%d %H:%M")
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_delete(request):
		project_id = request.POST['project_id']
		requirement_id = request.POST['requirement_id']
		comment_id = request.POST['comment_id']

		b_requirement = BRequirementRepository.get().get_requirement(project_id, requirement_id)
		b_requirement.delete_comment(comment_id)

		response = create_response(200)
		return response.get_response()