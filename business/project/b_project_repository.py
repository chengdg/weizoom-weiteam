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
from business.project.b_project import BProject
from util import db_util
from core import paginator


class BProjectRepository(business_model.Model):
	__slots__ = ()

	@staticmethod
	def get():
		"""工厂方法，获取repository对象
		"""
		repository = BProjectRepository()
		
		return repository
	
	def get_project_by_id(self, id):
		"""
		根据id获得project
		"""
		if not id:
			return None

		project_model = project_models.Project.objects.get(id=id)
		b_project = BProject.from_model(project_model)

		return b_project

	def get_projects_for_user(self, user):
		"""
		获取user参与的company集合
		"""
		user_project_relations = list(project_models.UserJoinProject.objects.filter(user=user))
		project_ids = [r.project_id for r in user_project_relations]
		project2relation = dict([(r.project_id, r) for r in user_project_relations])

		b_projects = []
		for project_model in project_models.Project.objects.filter(id__in=project_ids, is_deleted=False).order_by('-id'):
			b_project = BProject.from_model(project_model)
			user_project_relation = project2relation[project_model.id]
			if user_project_relation.is_manager:
				b_project.is_managed_by_user = True
			if user_project_relation.is_stared:
				b_project.is_stared_by_user = True
			b_projects.append(b_project)

		return b_projects

