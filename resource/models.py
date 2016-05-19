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

class Image(models.Model):
	"""
	上传的图片
	"""
	user = models.ForeignKey(User)
	path = models.CharField(max_length=1024, default='')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'resource_image'


class Document(models.Model):
	"""
	上传的文档
	"""
	user = models.ForeignKey(User)
	type = models.CharField(max_length=26) #文档类型
	filename = models.CharField(max_length=1024) #原始文件名
	path = models.CharField(max_length=1024, default='')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'resource_document'