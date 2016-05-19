# -*- coding: utf-8 -*-
from django.db.models import get_models, signals
from django.contrib.auth.models import User

from account import models as account_models

#===============================================================================
# init_wemanage : 初始化role与group
#===============================================================================
def init_wemanage(app, created_models, verbosity, **kwargs):
	# from django.contrib.auth.models import Permission
	# from django.contrib.auth.models import Group
	# from django.contrib.contenttypes.models import ContentType
	# from webapp.models import Workspace
	
	# #如果group_count大于1，意味着已经创建过role和group了，不用再次创建
	# group_count = Group.objects.count()
	# if group_count >= 1:
	# 	return
	
	# #创建Permission
	# ctype = ContentType.objects.get_for_model(Workspace)
	# manage_workspace_permission = Permission.objects.create(name="Can manage workspace", codename="manage_workspace", content_type=ctype)
	# ctype = ContentType.objects.get_for_model(User)
	# create_user_permission = Permission.objects.create(name="Can create user", codename="create_user", content_type=ctype)
	# print "Install custom permissions for weapp successfully"
	
	# #创建Group
	# g = Group.objects.create(name="Workspace_Manager")
	# g.permissions.add(manage_workspace_permission)
	# g = Group.objects.create(name="System_Agent")
	# g.permissions.add(create_user_permission)
	# print "Install custom permission groups for weapp successfully"

	# ContentType.objects.create(
	# 	name = u'SYSTEM_AUTH',
	# 	app_label = 'none',
	# 	model = 'none'
	# )
	pass


signals.post_syncdb.connect(init_wemanage, sender=account_models, dispatch_uid = "wemanage.init_wemanage")
	