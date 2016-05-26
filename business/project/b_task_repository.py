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
from business.project.b_task import BTask
from util import db_util
from core import paginator


class BTaskRepository(business_model.Model):
	__slots__ = ()

	@staticmethod
	def get():
		"""工厂方法，获取repository对象
		"""
		repository = BTaskRepository()
		
		return repository
	
	def get_task(self, task_id):
		"""
		获得默认迭代
		"""
		db_model = project_models.Task.objects.get(id=task_id)

		return BTask.from_model(db_model)
