# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import nav

class OutlineData(resource.Resource):
	app = 'outline'
	resource = 'outline_data'
	
	@login_required
	def api_get(request):
		"""
		响应GET
		"""

		time.sleep(0.5)
		response = create_response(200)
		response.data = {
			'name': 'outline',
			'value': '101.1'
		}

		return response.get_response()
