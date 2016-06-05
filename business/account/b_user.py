# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models as auth_models

import business.model as business_model
from business.decorator import cached_context_property
from account import models as account_models

class BUser(business_model.Model):
	__slots__ = (
		'id',
		'name',
		'thumbnail'
	)
	
	@staticmethod
	def from_model(user_db_model, profile_db_model):
		b_user = BUser()
		b_user.id = user_db_model.id
		b_user.name = user_db_model.first_name
		b_user.thumbnail = profile_db_model.thumbnail

		return b_user

	def __init__(self):
		pass