# -*- coding: utf-8 -*-

import os
import json
from hashlib import md5
from core.dateutil import get_current_time_in_millis

from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F

from core import dateutil
from project.models import Project


REQUIREMENT_TYPE_BUSINESS = 0
REQUIREMENT_TYPE_PRODUCT = 1
REQUIREMENT_TYPE_RD = 2
REQUIREMENT_STATUS_TODO = 0
REQUIREMENT_STATUS_DOING = 1
REQUIREMENT_STATUS_DONE = 2
class Requirement(models.Model):
	"""
	需求
	"""
	project = models.ForeignKey(Project, related_name='requirements')
	title = models.CharField(max_length=250) #任务标题
	content = models.TextField() #任务详情
	start_date = models.DateTimeField(auto_now_add=True) #任务启动时间
	enter_todo_date = models.DateTimeField(default='2000-01-01 00:00:00') #任务进入todo时间
	finish_date = models.DateTimeField(auto_now_add=True) #任务结束时间
	type = models.IntegerField() #需求类型
	status = models.IntegerField(default=0) #需求状态
	story_point = models.IntegerField(default=0) #故事点数
	importance = models.IntegerField(default=1) #需求重要度
	index = models.IntegerField(default=0)
	is_finished = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	creater = models.ForeignKey(User, related_name="created_requirements")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'requirement_requirement'


class RequirementComment(models.Model):
	"""
	需求评论
	"""
	creater = models.ForeignKey(User)
	requirement = models.ForeignKey(Requirement, related_name='comments')
	content = models.TextField() #任务详情
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'requirement_comment'