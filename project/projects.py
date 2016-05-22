# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.frontend_data import FrontEndData
from core.jsonresponse import create_response
from core import paginator
from util import db_util
import nav
import models
from business.project.b_project_repository import BProjectRepository

FIRST_NAV = 'project'

class Projects(resource.Resource):
	app = 'project'
	resource = 'projects'
	
	@login_required
	def get(request):		
		frontend_data = FrontEndData()
		project_datas = []
		b_projects = BProjectRepository.get().get_projects_for_user(request.user)
		for b_project in b_projects:
			project_datas.append({
				'id': b_project.id,
				'name': b_project.name,
				'description': b_project.description,
				'isManagedByUser': b_project.is_managed_by_user,
				'isStaredByUser': b_project.is_stared_by_user,
				'createdAt': b_project.created_at.strftime('%Y年%m月%d日')
			})
		frontend_data.add('projects', project_datas)
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'frontend_data': frontend_data
		})
		
		return render_to_response('project/projects.html', c)
