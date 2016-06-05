# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

import business.model as business_model
from requirement import models as requirement_models
from business.project.b_requirement import BRequirement
from business.account.b_user_repository import BUserRepository
from util import db_util
from core import paginator

COUNT_PER_PAGE = 2

class BRequirementRepository(business_model.Model):
	__slots__ = ()

	@staticmethod
	def get():
		"""工厂方法，获取repository对象
		"""
		repository = BRequirementRepository()
		
		return repository
	
	def get_requirement(self, project_id, requirement_id):
		"""
		获得project_id指定的project中的requirement
		"""
		db_model = requirement_models.Requirement.objects.get(project_id=project_id, id=requirement_id, is_deleted=False)

		return BRequirement.from_model(db_model)

	def __get_requirements(self, project_id, type, page, filter_options):
		"""
		获取需求集合
		"""
		requirements = requirement_models.Requirement.objects.filter(project_id=project_id, is_deleted=False, type=type)
		requirements = db_util.filter_query_set(requirements, filter_options)
		requirements = requirements.order_by('-id')
		pageinfo, requirements = paginator.paginate(requirements, page, COUNT_PER_PAGE)

		#批量填充creater
		creater_ids = [requirement.creater_id for requirement in requirements]
		b_users = BUserRepository.get().get_users(creater_ids)
		id2user = dict([(b_user.id, b_user) for b_user in b_users])

		b_requirements = []
		for requirement_db_model in requirements:
			b_requirement = BRequirement.from_model(requirement_db_model, False)
			b_requirement.creater = id2user[requirement_db_model.creater_id]
			b_requirements.append(b_requirement)

		return pageinfo, b_requirements

	def get_project_business_requirements(self, project_id, page, filter_options=None):
		"""
		获得业务需求集合
		"""
		return self.__get_requirements(project_id, requirement_models.REQUIREMENT_TYPE_BUSINESS, page, filter_options)

