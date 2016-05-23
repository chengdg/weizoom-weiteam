# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

import business.model as business_model
from project import models as project_models
from business.project.b_iteration import BIteration
from util import db_util
from core import paginator


class BIterationRepository(business_model.Model):
	__slots__ = ()

	@staticmethod
	def get():
		"""工厂方法，获取repository对象
		"""
		repository = BIterationRepository()
		
		return repository
	
	def get_default_iteration(self, project_id):
		"""
		获得默认迭代
		"""
		db_model = project_models.Iteration.objects.get(project_id=project_id, is_noiteration=True)

		return BIteration.from_model(db_model)

	def get_kanban_iteration(self):
		"""
		获得看板迭代
		"""
		db_model = project_models.Iteration.objects.get(project_id=project_id, is_maintaince=True)

		return BIteration.from_model(db_model)

