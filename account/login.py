# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response

class Login(resource.Resource):
	"""
	登录页面
	"""
	app = 'account'
	resource = 'login'
	
	def get(request):
		auth.logout(request)
		c = RequestContext(request, {})
		return render_to_response('account/login.html', c)
