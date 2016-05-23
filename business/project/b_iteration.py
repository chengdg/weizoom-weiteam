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
from project import models as project_models

class BIteration(business_model.Model):
	__slots__ = (
		'id',
		'start_date',
		'deadline',
		'description',
		'index',
		'is_closed',
		'is_maintaince',
		'created_at'
	)
	
	@staticmethod
	def from_model(db_model):
		iteration = BIteration(db_model)

		return iteration

	@staticmethod
	def create_kanban(project):
		iteration = project_models.Iteration.objects.create(
			deadline = '3000-01-01 00:00:00',
			project = project,
			description = '团队看板',
			index = 1,
			is_closed = True,
			is_maintaince = True
		)

		return BIteration(iteration)

	@staticmethod
	def create_default_iteration(project):
		iteration = project_models.Iteration.objects.create(
			deadline = '3000-01-01 00:00:00',
			project = project,
			description = 'noiteartion',
			index = 0,
			is_noiteration = True
		)

		return BIteration(iteration)

	@staticmethod
	def create(options):
		iteration = project_models.Iteration.objects.create(
			start_date = options['start_date'],
			deadline = options['deadline'],
			project_id = options['project_id'],
			description = options['description']
		)

		return BIteration(iteration)

	def __init__(self, model=None):
		business_model.Model.__init__(self)
		self._init_slot_from_model(model)

	def delete(self):
		pass