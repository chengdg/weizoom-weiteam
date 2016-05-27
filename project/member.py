# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import models as auth_models

from core import resource
from core.jsonresponse import create_response
from core.frontend_data import FrontEndData
from account import models as account_models
from business.project.b_project_repository import BProjectRepository

FIRST_NAV = 'member'

class Member(resource.Resource):
	"""
	用户
	"""
	app = 'project'
	resource = 'member'
	
	@login_required
	def api_put(request):
		project_id = request.POST['project_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)

		user_ids = json.loads(request.POST['user_ids'])
		b_project.add_members(user_ids)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		project_id = request.POST['project_id']
		member_id = request.POST['member_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)
		b_project.delete_member(member_id)

		response = create_response(200)
		return response.get_response()
