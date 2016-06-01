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
from requirement import models as requirement_models
from business.project.b_iteration import BIteration
from business.project.b_iteration_repository import BIterationRepository
from business.project.b_stage import BStage
from business.project.b_stage_repository import BStageRepository
from business.project.b_task import BTask
from util import db_util
from core import paginator

MANAGER_GROUP_ID = 1
COUNT_PER_PAGE = 2

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
			is_manager = True,
			is_creater = True
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
	def creater(self):
		"""
		project的创建者
		"""
		user_join_project = project_models.UserJoinProject.objects.get(project_id=self.id, is_creater=True)
		return auth_models.User.objects.get(id=user_join_project.user_id)

	def is_creater(self, user):
		"""
		判断user是否是project的creater
		"""
		user_join_project = project_models.UserJoinProject.objects.get(project_id=self.id, is_creater=True)
		return user.id == user_join_project.user_id

	def is_manager(self, user):
		"""
		判断user是否是project的manager
		"""
		user_join_project = project_models.UserJoinProject.objects.get(project_id=self.id, is_manager=True)
		return user.id == user_join_project.user_id

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

	@property
	def members(self):
		joined_infos = [r for r in project_models.UserJoinProject.objects.filter(project_id=self.id)]
		joined_member_ids = [info.user_id for info in joined_infos]
		user2info = dict([(info.user_id, info) for info in joined_infos])

		users = list(auth_models.User.objects.filter(id__in=joined_member_ids, is_active=True))
		members = []
		for user in users:
			user.name = user.first_name
			join_info = user2info[user.id]
			user.is_manager = join_info.is_manager
			user.join_time = join_info.id
			profile = user.get_profile()
			user.thumbnail = profile.thumbnail
			members.append(user)
		members.sort(lambda x,y: cmp(y.join_time, x.join_time))

		return members

	@property
	def candidate_members(self):
		users = list(auth_models.User.objects.filter(id__gt=3, is_active=True))
		joined_members = set([r.user_id for r in project_models.UserJoinProject.objects.filter(project_id=self.id)])

		members = []
		for user in users:
			if not user.id in joined_members:
				user.name = user.first_name
				members.append(user)

		return members

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

	def add_members(self, user_ids):
		"""
		添加一组用户作为project的成员
		"""
		for user_id in user_ids:
			project_models.UserJoinProject.objects.create(
				user_id = user_id,
				project_id = self.id
			)

	def delete_member(self, member_id):
		"""
		从project中删除一个成员
		"""
		project_models.UserJoinProject.objects.filter(project_id=self.id, user_id=member_id).delete()

	def get_user_permissions(self, user):
		"""
		填充用户操作project的权限
		"""
		user_join_project = project_models.UserJoinProject.objects.get(project_id=self.id, user_id=user.id)
		permissions = []
		if user_join_project.is_manager:
			permissions.append('manage_project')

		return permissions

	def delete_requirement(self, requirement_id):
		"""
		删除需求
		"""
		project_models.Task.objects.filter(id=requirement_id).update(is_deleted=True)

	def get_business_requirements(self, page, filter_options=None):
		"""
		获取project的业务需求集合
		"""
		requirements = requirement_models.Requirement.objects.filter(project_id=self.id, is_deleted=False, type=requirement_models.REQUIREMENT_TYPE_BUSINESS)
		requirements = db_util.filter_query_set(requirements, filter_options)
		requirements = requirements.order_by('-id')
		pageinfo, requirements = paginator.paginate(requirements, page, COUNT_PER_PAGE)

		#批量填充creater
		creater_ids = [requirement.creater_id for requirement in requirements]
		id2user = dict([(user.id, user) for user in auth_models.User.objects.filter(id__in=creater_ids)])
		for requirement in requirements:
			requirement.creater = id2user[requirement.creater_id]

		return pageinfo, requirements

	def get_business_requirement(self, requirement_id):
		"""
		获取project中指定的业务需求
		"""
		requirement = requirement_models.Requirement.objects.get(id=requirement_id, is_deleted=False, type=requirement_models.REQUIREMENT_TYPE_BUSINESS)

		return requirement

	def add_business_requirement(self, options):
		"""
		向project中添加business_requirment
		"""
		requirement = requirement_models.Requirement.objects.create(
			project_id = self.id,
			creater = options['owner'],
			title = options['title'],
			content = options['content'],
			type = requirement_models.REQUIREMENT_TYPE_BUSINESS,
			importance = options['importance']
		)

		return requirement

	def delete_business_requirement(self, requirement_id):
		"""
		删除project中requirement_id指定的business_requirment
		"""
		requirement_models.Requirement.objects.filter(id=requirement_id).update(is_deleted=True)

	def update_business_requirement(self, requirement_id, field, value):
		"""
		更新business_requirement的属性
		"""
		options = {
			field: value
		}
		requirement_models.Requirement.objects.filter(id=requirement_id).update(**options)
		return True
