# -*- coding: utf-8 -*-

#
# 配置，使behave能使用django的model
#
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'wemanage.settings'

import sys
path = os.path.abspath(os.path.join('.', '..'))
sys.path.insert(0, path)

import unittest
from pymongo import Connection

from wemanage import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test.client import Client
from django.test.utils import setup_test_environment as setup_django_test_environment
from django.db.models import Q

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import bdd_util

from account import models as account_models

def __clear_all_account_data():
	"""
	清空账号数据
	"""
	User.objects.filter(id__gt=3).delete()


clean_modules = []
def __clear_all_app_data():
	"""
	清空应用数据
	"""
	if len(clean_modules) == 0:
		for clean_file in os.listdir('./features/clean'):
			if clean_file.startswith('__'):
				continue

			module_name = 'features.clean.%s' % clean_file[:-3]
			module = __import__(module_name, {}, {}, ['*',])	
			clean_modules.append(module)

	for clean_module in clean_modules:
		clean_module.clean()


def __create_system_user(username):
	"""
	创建系统用户
	"""
	user = User.objects.create_user(username=username, email='a@a.com', password='test')
	return user	


def before_all(context):
	__clear_all_account_data()
	__create_system_user('jobs')
	__create_system_user('bill')
	__create_system_user('tom')
	__create_system_user('nokia')

	#创建test case，使用assert
	context.tc = unittest.TestCase('__init__')
	import bdd_util
	bdd_util.tc = context.tc

	#设置django为测试状态
	setup_django_test_environment()

	#为model instance安装__getitem__，方便测试
	enhance_django_model_class()

	#设置bdd模式
	settings.IS_UNDER_BDD = True


def after_all(context):
	pass


def before_scenario(context, scenario):
	is_ui_test = False
	context.scenario = scenario
	for tag in scenario.tags:
		if tag.startswith('ui-') or tag == 'ui':
			is_ui_test = True
			break

	if is_ui_test:
		#创建浏览器
		print('[before scenario]: init browser driver')
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument("--disable-plugins")
		driver = webdriver.Chrome(chrome_options=chrome_options)
		driver.implicitly_wait(3)
		context.driver = driver

	__clear_all_app_data()


def after_scenario(context, scenario):
	if hasattr(context, 'client') and context.client:
		context.client.logout()

	if hasattr(context, 'driver') and context.driver:
		print('[after scenario]: close browser driver')
		#page_frame = PageFrame(context.driver)
		#page_frame.logout()
		context.driver.quit()

	if hasattr(context, 'webapp_driver') and context.driver:
		print('[after scenario]: close webapp browser driver')
		context.webapp_driver.quit()


#
# 为Django model添加__getitem__
#
def enhance_django_model_class():
	from django.db.models import Model

	#def model_getitem(self, key):
	#	return getattr(self, key)
	#Model.__getitem__ = model_getitem

	def model_todict(self):
		columns = [field.get_attname() for field in self._meta.fields]
		result = {}
		for field in self._meta.fields:
			result[field.get_attname()] = field.value_to_string(self)
		return result
	Model.to_dict = model_todict
