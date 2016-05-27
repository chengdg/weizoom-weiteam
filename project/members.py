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

class Members(resource.Resource):
	"""
	项目成员集合
	"""
	app = 'project'
	resource = 'members'
	
	@login_required
	def get(request):
		project_id = request.GET['project_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)
		creater = b_project.creater

		members = []
		for member in b_project.members:
			members.append({
				'id': member.id,
				'name': member.name,
				'thumbnail': member.thumbnail,
				'isManager': member.is_manager,
				'isCreater': member.id == creater.id
			})

		frontend_data = FrontEndData()
		frontend_data.add('members', members)
		frontend_data.add('projectId', project_id)
		frontend_data.add_user_permissions(b_project.get_user_permissions(request.user))
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'frontend_data': frontend_data
		})
		
		return render_to_response('project/members.html', c)
