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

class Product(models.Model):
	"""
	商品
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=1024)
	price = models.FloatField(default=0.0)
	weight = models.IntegerField(default=0)
	comment = models.CharField(max_length=1024, default='')
	is_join_promotion = models.BooleanField(default=False)
	promotion_finish_time = models.DateTimeField()
	channels = models.CharField(max_length=1024, default='')
	detail = models.TextField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'outline_product'


class ProductModel(models.Model):
	"""
	商品规格
	"""
	product = models.ForeignKey(Product)
	name = models.CharField(max_length=1024)
	stocks = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'outline_product_model'


class ProductImage(models.Model):
	"""
	商品图片
	"""
	product = models.ForeignKey(Product)
	image_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'outline_product_image'


class ProductDocument(models.Model):
	"""
	商品文档
	"""
	product = models.ForeignKey(Product)
	document_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'outline_product_document'