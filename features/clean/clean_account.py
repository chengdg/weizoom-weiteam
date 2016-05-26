# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.models import User

def clean():
	logging.info('clean database for account app')
	if User.objects.filter(username='guojing').exists():
		guojing = User.objects.get(username='guojing')
		User.objects.filter(id__gte=guojing.id).delete()
