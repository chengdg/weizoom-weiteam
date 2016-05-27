# -*- coding: utf-8 -*-

import json

class FrontEndData(object):
	def __init__(self):
		self.jsons = {'items':[]}

	def add(self, name, value):
		self.jsons['items'].append((name, json.dumps(value)))

	def add_user_permissions(self, permissions):
		self.add('__userPermissions', permissions)

	def get(self, name):
		for item in self.jsons['items']:
			if item[0] == name:
				return json.loads(item[1])