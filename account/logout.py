# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.conf import settings

from core import resource
from core.jsonresponse import create_response

class Logout(resource.Resource):
	"""
	登录页面
	"""
	app = 'account'
	resource = 'logout'
	
	def get(request):
		auth.logout(request)
		return HttpResponseRedirect('/account/login/')
