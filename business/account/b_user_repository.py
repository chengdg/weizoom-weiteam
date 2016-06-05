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
from business.account.b_user import BUser
from util import db_util
from core import paginator
from account import models as account_models


class BUserRepository(business_model.Model):
	__slots__ = ()

	@staticmethod
	def get():
		"""
		工厂方法，获取repository对象
		"""
		repository = BUserRepository()
		
		return repository
	
	def get_user(self, user_id):
		"""
		获得用户
		"""
		user_db_model = auth_models.User.objects.get(id=user_id)
		profile_db_model = account_models.UserProfile.objects.get(user_id=user_id)

		return BUser.from_model(user_db_model, profile_db_model)

	def get_users(self, user_ids):
		"""
		获得用户
		"""
		user_db_models = auth_models.User.objects.filter(id__in=user_ids)
		profile_db_models = account_models.UserProfile.objects.filter(user_id__in=user_ids)
		user2profile = dict([(profile.user_id, profile) for profile in profile_db_models])

		b_users = []
		for user_db_model in user_db_models:
			profile_db_model = user2profile[user_db_model.id]
			b_users.append(BUser.from_model(user_db_model, profile_db_model))

		return b_users