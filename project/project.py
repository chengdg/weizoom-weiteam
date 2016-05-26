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
from business.project.b_project import BProject
from business.project.b_project_repository import BProjectRepository

FIRST_NAV = 'project'

class Project(resource.Resource):
	app = 'project'
	resource = 'project'
	
	@login_required
	def get(request):
		project_id = request.GET.get('id', None)
		b_project = BProjectRepository.get_project_by_id(project_id)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV
		})
		
		return render_to_response('project/project.html', c)

	@login_required
	def api_get(request):
		project_id = request.GET.get('id', None)
		b_project = BProjectRepository.get().get_project_by_id(project_id)

		response = create_response(200)
		response.data = {
			'id': b_project.id,
			'name': b_project.name,
			'description': b_project.description
		}

		return response.get_response()

	@login_required
	def api_put(request):
		name = request.POST['name']
		description = request.POST['description']
		b_project = BProject.create(request.user, name, description)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		project_id = request.POST['id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)
		b_project.update(request.POST['name'], request.POST['description'])

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		project_id = request.POST['id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)
		b_project.delete()

		response = create_response(200)
		return response.get_response()