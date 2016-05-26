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

class BTask(business_model.Model):
	__slots__ = (
		'id',
		'type',
		'is_shared',
		'manager',
		'title',
		'content',
		'start_date',
		'enter_todo_date',
		'deadline',
		'finish_date',
		'story_point',
		'importance',
		'index',
		'is_finished',
		'is_deleted',
		'creater',
		'created_at'
	)
	
	@staticmethod
	def from_model(db_model):
		task = BTask(db_model)

		return task

	@staticmethod
	def create(options):
		task = None

		return task

	@staticmethod
	def create_requirement(options):
		task = project_models.Task.objects.create(
			project_id = options['project_id'],
			iteration_id = options['iteration_id'],
			stage_id = options['stage_id'],
			title = options['title'],
			content = options['content'],
			type = project_models.TASK_TYPE_REQUIREMENT,
			importance = options['importance'],
			manager = options['owner'],
			creater = options['owner']
		)

		return BTask.from_model(task)

	def __init__(self, model=None):
		business_model.Model.__init__(self)
		self._init_slot_from_model(model)
		self.context['db_model'] = model

	def delete(self):
		pass

	def update(self, field, value):
		"""
		更新task的属性
		"""
		options = {
			field: value
		}
		project_models.Task.objects.filter(id=self.id).update(**options)
		return True