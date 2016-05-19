# -*- coding: utf-8 -*-

import sys
import os
import traceback
import StringIO
import cProfile
import time
import types
from django.conf import settings
from datetime import timedelta, datetime, date

from django.core.urlresolvers import ResolverMatch, Resolver404
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings


APPRESOURCE2CLASS = dict()
RESTFUL_APP_SET = set()

JS_TMPL = """

ensureNS("W.resource.%(normalized_app)s");
W.resource.%(normalized_app)s.%(cls)s = new W.resource.Resource({
	app: '%(app)s',
	resource: '%(resource)s'
});"""

class ResourceBase(type):
	def __new__(cls, name, bases, attrs):
		return super(ResourceBase, cls).__new__(cls, name, bases, attrs)

	def __init__(self, name, bases, attrs):
		if name == 'Resource':
			pass
		else:
			app_resource = '%s-%s' % (self.app, self.resource)
			print '[resource] register resource: ', app_resource
			RESTFUL_APP_SET.add('/%s/' % self.app)
			for key, value in self.__dict__.items():
				if hasattr(value, '__call__'):
					static_method = staticmethod(value)
					setattr(self, key, static_method)

			APPRESOURCE2CLASS[app_resource] = {
				'cls': self,
				'instance': None,
				# 'js': JS_TMPL % {
				# 	"app": self.app,
				# 	"normalized_app": self.app.replace('/', '.'),
				# 	"resource": self.resource,
				# 	"cls": name
				# }
			}
		super(ResourceBase, self).__init__(name, bases, attrs)


class Resource(object):
	__metaclass__ = ResourceBase

	