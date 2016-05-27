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

class Project(models.Model):
	"""
	项目看板
	"""
	name = models.CharField(max_length=20)
	members = models.ManyToManyField(User, through='UserJoinProject', related_name='joined_projects')
	description = models.CharField(max_length=100)
	use_email_notification = models.BooleanField(default=False)
	use_im_notification = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

	class Meta(object):
		db_table = 'project_project'


class UserJoinProject(models.Model):
	"""
	用户参与项目的情况
	"""
	user = models.ForeignKey(User)
	project = models.ForeignKey(Project)
	is_stared = models.BooleanField(default=False)
	is_manager = models.BooleanField(default=False)
	is_creater = models.BooleanField(default=False)

	def __unicode__(self):
		return '<%s, %s>' % (self.user.username, self.project.name)

	class Meta(object):
		db_table = 'project_user_join_project'


class Iteration(models.Model):
	"""
	迭代
	"""
	start_date = models.DateTimeField(auto_now_add=True)
	deadline = models.DateTimeField()
	project = models.ForeignKey(Project, related_name='iterations')
	description = models.TextField()
	index = models.IntegerField()
	#for normal iteration, this indicate whether it was closed
	#for maintaince iteration this always is True
	is_closed = models.BooleanField(default=False)
	is_maintaince = models.BooleanField(default=False)
	is_noiteration = models.BooleanField(default=False) #是否是容纳不在有效iteration中的任务的iteartion
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.description

	class Meta(object):
		db_table = 'project_iteration'
		ordering = ["-deadline"]


class Stage(models.Model):
	"""
	价值流阶段
	"""
	project = models.ForeignKey(Project, related_name="project_stages")
	name = models.CharField(max_length=256) #阶段名
	is_finish_stage = models.BooleanField(default=False) #是否是"已完成"stage
	is_buffer_stage = models.BooleanField(default=False) #是否是缓冲stage，缓冲stage中的task不计入WIP
	wip_container = models.CharField(max_length=256, default='') #wip所属的组
	wip_count = models.IntegerField(default=0) #阶段的wip数
	display_index = models.IntegerField(default=0) #排序

	class Meta(object):
		db_table = 'project_stage'


TASK_TYPE_TASK = 0
TASK_TYPE_BUG = 1
TASK_TYPE_REQUIREMENT = 2
TASK_TYPE_TEST = 3
TASK_TYPE_DEPLOYMENT = 4
TASK_PRIORITY_LOW = 1
TASK_PRIORITY_NORMAL = 2
TASK_PRIORITY_HIGH = 3
TASK_TODO = 0
TASK_DOING = 1
TASK_DONE = 2
class Task(models.Model):
	"""
	任务
	"""
	project = models.ForeignKey(Project, related_name='tasks')
	iteration = models.ForeignKey(Iteration, related_name='tasks')
	stage = models.ForeignKey(Stage, related_name='stage_tasks')
	root_task_id = models.IntegerField(default=0) #root任务
	is_shared = models.BooleanField(default=False) #是否已分享
	manager = models.ForeignKey(User, related_name='managed_tasks')
	title = models.CharField(max_length=250) #任务标题
	content = models.TextField() #任务详情
	start_date = models.DateTimeField(auto_now_add=True) #任务启动时间
	enter_todo_date = models.DateTimeField(default='2000-01-01 00:00:00') #任务进入todo时间
	deadline = models.DateTimeField(auto_now_add=True) #任务deadline
	finish_date = models.DateTimeField(auto_now_add=True) #任务结束时间
	type = models.IntegerField() #任务类型
	priority = models.IntegerField(default=TASK_PRIORITY_NORMAL) #任务优先级
	story_point = models.IntegerField(default=0) #故事点数
	importance = models.IntegerField(default=1) #任务重要度
	index = models.IntegerField(default=0)
	is_finished = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)
	#owner_requirement = models.IntegerField(default=0)
	creater = models.ForeignKey(User, related_name="created_tasks")
	#related_requirement_id = models.IntegerField(default=0) #关联的需求的id
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'project_task'