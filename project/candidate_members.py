# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User

from core import resource
from core.jsonresponse import create_response
from core.frontend_data import FrontEndData
from business.project.b_project_repository import BProjectRepository

FIRST_NAV = 'member'

class CandidateMembers(resource.Resource):
	"""
	项目候选成员集合
	"""
	app = 'project'
	resource = 'candidate_members'
	
	@login_required
	def api_get(request):
		project_id = request.GET['project_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)

		members = []
		for member in b_project.candidate_members:
			members.append({
				'id': member.id,
				'name': member.name
			})

		response = create_response(200)
		response.data = {
			'members': members
		}

		return response.get_response()