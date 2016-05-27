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

class Requirements(resource.Resource):
	app = 'project'
	resource = 'requirements'
	
	@login_required
	def get(request):
		project_id = request.GET['project_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)

		frontend_data = FrontEndData()
		frontend_data.add('projectId', project_id)
		frontend_data.add_user_permissions(b_project.get_user_permissions(request.user))
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'frontend_data': frontend_data
		})
		
		return render_to_response('project/requirements.html', c)

	@login_required
	def api_get(request):
		#获取业务数据
		project_id = request.GET['project_id']
		cur_page = request.GET.get('page', 1)
		tasks = models.Task.objects.filter(project_id=project_id, is_deleted=False, type=models.TASK_TYPE_REQUIREMENT)
		tasks = db_util.filter_query_set(tasks, request)
		tasks = tasks.order_by('-id')
		pageinfo, tasks = paginator.paginate(tasks, cur_page, COUNT_PER_PAGE)

		#组装数据
		rows = []
		for task in tasks:
			rows.append({
				'id': task.id,
				'title': task.title,
				'importance': task.importance,
				'storyPoint': task.story_point,
				'creater': task.creater.first_name,
				'tags': [],
				'createdAt': task.created_at.strftime('%Y.%m.%d')
			})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()
