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

FIRST_NAV = 'kanban'

class Kanban(resource.Resource):
	app = 'project'
	resource = 'kanban'
	
	@login_required
	def get(request):
		project_id = request.GET.get('id', None)
		b_project = BProjectRepository.get().get_project_by_id(project_id)

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV
		})
		
		return render_to_response('project/kanban.html', c)