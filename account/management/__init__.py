# -*- coding: utf-8 -*-
from django.db.models import get_models, signals
from django.contrib.auth.models import User

from account import models as account_models

#===============================================================================
# init_weteam : 初始化role与group
#===============================================================================
def init_weteam(app, created_models, verbosity, **kwargs):
	from django.contrib.auth.models import Permission
	from django.contrib.auth.models import Group
	from django.contrib.contenttypes.models import ContentType
	
	#如果group_count大于1，意味着已经创建过role和group了，不用再次创建
	group_count = Group.objects.count()
	if group_count >= 1:
		return

	#创建content type
	ctype = ContentType.objects.create(
		name = u'MANAGE_SYSTEM',
		app_label = 'permission',
		model = 'permission'
	)
	
	#管理员组
	g = Group.objects.create(name="SystemManager")
	manage_system_permission = Permission.objects.create(name="Can manage system", codename="__manage_system", content_type=ctype)
	g.permissions.add(manage_system_permission)
	#研发
	g = Group.objects.create(name="RD")
	permission = Permission.objects.create(name="研发权限", codename="__manage_rd", content_type=ctype)
	g.permissions.add(permission)
	#测试
	g = Group.objects.create(name="QA")
	permission = Permission.objects.create(name="测试权限", codename="__manage_qa", content_type=ctype)
	g.permissions.add(permission)
	#Devop
	g = Group.objects.create(name="devop")
	permission = Permission.objects.create(name="DevOp权限", codename="__manage_devop", content_type=ctype)
	g.permissions.add(permission)
	#产品
	g = Group.objects.create(name="PM")
	permission = Permission.objects.create(name="产品权限", codename="__manage_pm", content_type=ctype)
	g.permissions.add(permission)
	#业务部门
	g = Group.objects.create(name="BU")
	permission = Permission.objects.create(name="业务人员权限", codename="__manage_bu", content_type=ctype)
	g.permissions.add(permission)

	print "Install custom permission groups for weteam successfully"


signals.post_syncdb.connect(init_weteam, sender=account_models, dispatch_uid = "weteam.init_weteam")
	