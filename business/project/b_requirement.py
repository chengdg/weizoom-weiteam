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
from requirement import models as requirement_models
from account import models as account_models
from business.account.b_user_repository import BUserRepository

class BRequirement(business_model.Model):
	__slots__ = (
		'id',
		'title',
		'content',
		'manager',
		'title',
		'content',
		'start_date',
		'finish_date',
		'importance',
		'is_finished',
		'is_deleted',
		'creater',
		'created_at'
	)
	
	@staticmethod
	def from_model(db_model, fill_creater=True):
		requirement = BRequirement(db_model, fill_creater)

		return requirement

	@staticmethod
	def __create_requirement(options):
		requirement = requirement_models.Requirement.objects.create(
			project_id = options['project_id'],
			creater = options['owner'],
			title = options['title'],
			content = options['content'],
			type = options['type'],
			importance = options['importance']
		)

		return requirement

	@staticmethod
	def create_business_requirement(options):
		"""
		向project中添加business_requirment
		"""
		options['type'] = requirement_models.REQUIREMENT_TYPE_BUSINESS
		requirement = BRequirement.__create_requirement(options)

		return BRequirement(requirement)

	def __init__(self, model=None, fill_creater=True):
		business_model.Model.__init__(self)
		self._init_slot_from_model(model)
		self.context['db_model'] = model

		if fill_creater:
			self.creater = BUserRepository.get_user(model.creater_id)

	def delete(self):
		"""
		删除requirment
		"""
		requirement_models.Requirement.objects.filter(id=self.id).update(is_deleted=True)

	def update(self, field, value):
		"""
		更新requirement的属性
		"""
		options = {
			field: value
		}
		requirement_models.Requirement.objects.filter(id=self.id).update(**options)