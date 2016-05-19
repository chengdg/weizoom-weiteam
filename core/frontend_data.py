# -*- coding: utf-8 -*-

import json

class FrontEndData(object):
	def __init__(self):
		self.jsons = {'items':[]}

	def add(self, name, value):
		self.jsons['items'].append((name, json.dumps(value)))