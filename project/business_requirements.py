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

FIRST_NAV = 'requirement'
COUNT_PER_PAGE = 2

class BusinessRequirements(resource.Resource):
	app = 'project'
	resource = 'business_requirements'
	
	@login_required
	def get(request):
		project_id = request.GET['project_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)

		frontend_data = FrontEndData()
		frontend_data.add('projectId', project_id)
		frontend_data.add_user_permissions(b_project.get_user_permissions(request.user))
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_requirement_second_navs(project_id),
			'second_nav_name': 'project-business-requirements', 
			'frontend_data': frontend_data
		})
		
		return render_to_response('project/business_requirements.html', c)

	@login_required
	def api_get(request):
		project_id = request.GET['project_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)

		cur_page = request.GET.get('page', 1)
		pageinfo, requirements = b_project.get_business_requirements(cur_page, request.GET)
		
		#组装数据
		rows = []
		for requirement in requirements:
			rows.append({
				'id': requirement.id,
				'title': requirement.title,
				'importance': requirement.importance,
				'creater': requirement.creater.first_name,
				'subRequirements': 0,
				'storyPoint': 0,
				'createdAt': requirement.created_at.strftime('%Y.%m.%d')
			})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()
