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

class BStage(business_model.Model):
	__slots__ = (
		'id',
		'name',
		'is_finish_stage',
		'is_buffer_stage',
		'wip_container',
		'display_index'
	)
	
	@staticmethod
	def from_model(db_model):
		stage = BStage(db_model)

		return stage

	@staticmethod
	def create_default_stages(project):
		project_models.Stage.objects.create(
			project = project,
			name = 'project_default'
		)

		stages = [
			{"name": u"TODO", "is_buffer_stage": True, "is_finish_stage": False, "wip_container": u"TODO", "wip_count": 8, "display_index": 1},
			{"name": u"设计", "is_buffer_stage": False, "is_finish_stage": False, "wip_container": u"设计", "wip_count": 3, "display_index": 2},
			{"name": u"待开发", "is_buffer_stage": True, "is_finish_stage": False, "wip_container": u"设计", "wip_count": 0, "display_index": 3},
			{"name": u"开发", "is_buffer_stage": False, "is_finish_stage": False, "wip_container": u"开发", "wip_count": 4, "display_index": 4},
			{"name": u"待测试", "is_buffer_stage": True, "is_finish_stage": False, "wip_container": u"开发", "wip_count": 0, "display_index": 5},
			{"name": u"测试", "is_buffer_stage": False, "is_finish_stage": False, "wip_container": u"测试", "wip_count": 2, "display_index": 6},
			{"name": u"已完成", "is_buffer_stage": True, "is_finish_stage": True, "wip_container": u"已完成", "wip_count": 0, "display_index": 7},
		]

		#创建研发通用Stage
		for stage in stages:
			project_models.Stage.objects.create(
				project = project,
				name = stage['name'],
				is_finish_stage = stage['is_finish_stage'],
				is_buffer_stage = stage['is_buffer_stage'],
				wip_container = stage['wip_container'],
				wip_count = stage['wip_count'],
				display_index = stage['display_index']
			)

	def __init__(self, model=None):
		business_model.Model.__init__(self)
		self._init_slot_from_model(model)

	def delete(self):
		pass