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

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	thumbnail = models.CharField(max_length=256, default='/static/img/default_user.jpg') #用户头像
	wip_count = models.IntegerField(default=1) #当前的wip值

	class Meta(object):
		db_table = 'account_user_profile'
		verbose_name = '用户配置'
		verbose_name_plural = '用户配置'

	@property
	def is_manager(self):
		return (self.user_id == self.manager_id) or (self.manager_id == 2) #2 is manager's id


def create_profile(instance, created, **kwargs):
	"""
	自动创建user profile
	"""
	if created:
		if instance.username == 'admin':
			return
		if UserProfile.objects.filter(user=instance).count() == 0:
			profile = UserProfile.objects.create(user = instance)
			

signals.post_save.connect(create_profile, sender=User, dispatch_uid = "account.create_profile")