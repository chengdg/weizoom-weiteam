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
from business.project.b_iteration import BIteration
from business.project.b_iteration_repository import BIterationRepository
from business.project.b_stage import BStage
from business.project.b_stage_repository import BStageRepository
from business.project.b_task import BTask

MANAGER_GROUP_ID = 1

class BProject(business_model.Model):
	__slots__ = (
		'id',
		'name',
		'description',
		'is_delete',
		'is_managed_by_user',
		'is_stared_by_user',
		'created_at'
	)
	
	@staticmethod
	def from_model(db_model):
		project = BProject(db_model)

		return project

	@staticmethod
	def create(owner, name, description):
		project = project_models.Project.objects.create(
			name = name,
			description = description
		)

		project_models.UserJoinProject.objects.create(
			user = owner,
			project = project,
			is_manager = True
		)

		BStage.create_default_stages(project)
		BIteration.create_default_iteration(project)
		BIteration.create_kanban(project)

		return project

	def __init__(self, model=None):
		business_model.Model.__init__(self)
		self._init_slot_from_model(model)
		self.is_managed_by_user = False
		self.is_stared_by_user = False

	def delete(self):
		project_models.Project.objects.filter(id=self.id).update(is_deleted=True)

	@property
	def status(self):
		group_name = self.charge_group.name
		if group_name == 'SystemManager':
			return u'抢单中'
		elif group_name == 'Operation':
			return u'运营服务中'
		elif group_name == 'WeizoomFamily':
			return u'微众家服务中'
		else:
			return u'未知'

	def update(self, name, description):
		"""
		更新团队信息
		"""
		project_models.Project.objects.filter(id=self.id).update(name=name, description=description)

	def star_by_user(self, user):
		"""
		user将project加星
		"""
		project_models.UserJoinProject.objects.filter(id=self.id, user=user).update(is_stared=True)

	def unstar_by_user(self, user):
		"""
		user将project取消加星
		"""
		project_models.UserJoinProject.objects.filter(id=self.id, user=user).update(is_stared=False)

	def add_requirement(self, options):
		"""
		向project中添加requirment
		"""
		options['project_id'] = self.id
		options['iteration_id'] = BIterationRepository.get().get_default_iteration(self.id).id
		options['stage_id'] = BStageRepository.get().get_default_stage(self.id).id
		BTask.create_requirement(options)