# -*- coding: utf-8 -*-

import sys
import json

def raw_html(str):
	return str.replace('<', '&lt;').replace('>', '&gt;')
