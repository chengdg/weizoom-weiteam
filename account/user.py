# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import models as auth_models

from core import resource
from core.jsonresponse import create_response
from core.frontend_data import FrontEndData
from account import models as account_models

FIRST_NAV = 'account'

class User(resource.Resource):
	"""
	用户
	"""
	app = 'account'
	resource = 'user'
	
	@login_required
	def api_put(request):
		username = request.POST['name']
		real_name = request.POST['real_name']
		email = request.POST['email']
		password = request.POST['password']
		if not password:
			password = 'weizoom'
		thumbnail = request.POST['thumbnail']
		if not thumbnail:
			thumbnail = '/static/img/default_user.jpg'

		user = auth_models.User.objects.create_user(username, email=email, password=password, first_name=real_name)
		account_models.UserProfile.objects.filter(user_id=user.id).update(thumbnail=thumbnail)

		response = create_response(200)
		response.data = {
			'id': user.id,
			'name': user.username,
			'realName': user.first_name,
			'email': user.email,
			'thumbnail': thumbnail
		}
		return response.get_response()

	@login_required
	def api_post(request):
		id = request.POST['id']
		username = request.POST['name']
		real_name = request.POST['real_name']
		email = request.POST['email']
		thumbnail = request.POST['thumbnail']
		if not thumbnail:
			thumbnail = '/static/img/default_user.jpg'

		auth_models.User.objects.filter(id=id).update(email=email, username=username, first_name=real_name)
		account_models.UserProfile.objects.filter(user_id=id).update(thumbnail=thumbnail)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		id = request.POST['id']
		
		auth_models.User.objects.filter(id=id).update(is_active=False)

		response = create_response(200)
		return response.get_response()
