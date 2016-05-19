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


class StaredProject(models.Model):
	"""
	关注项目
	"""
	owner = models.ForeignKey(User)
	project = models.ForeignKey(Project)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'project_stared_project'


class UserJoinProject(models.Model):
	user = models.ForeignKey(User)
	project = models.ForeignKey(Project)
	is_manager = models.BooleanField(default=False)

	def __unicode__(self):
		return '<%s, %s>' % (self.user.username, self.project.name)

	class Meta(object):
		db_table = 'project_user_join_project'