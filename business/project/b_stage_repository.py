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
from business.project.b_stage import BStage
from util import db_util
from core import paginator


class BStageRepository(business_model.Model):
	__slots__ = ()

	@staticmethod
	def get():
		"""工厂方法，获取repository对象
		"""
		repository = BStageRepository()
		
		return repository
	
	def get_default_stage(self, project_id):
		"""
		获得默认迭代
		"""
		db_model = project_models.Stage.objects.get(project_id=project_id, name='project_default')

		return BStage.from_model(db_model)
