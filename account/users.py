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

FIRST_NAV = 'account'

class Users(resource.Resource):
	"""
	用户集合
	"""
	app = 'account'
	resource = 'users'
	
	@login_required
	def get(request):
		users = []
		for user in User.objects.filter(id__gt=3, is_active=True).order_by('-id'):
			profile = user.get_profile()
			users.append({
				'id': user.id,
				'name': user.username,
				'realName': user.first_name,
				'email': user.email,
				'thumbnail': profile.thumbnail
			})

		frontend_data = FrontEndData()
		frontend_data.add('users', users)
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'frontend_data': frontend_data
		})
		
		return render_to_response('account/users.html', c)
