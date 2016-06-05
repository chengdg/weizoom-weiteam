# -*- coding: utf-8 -*-

import sys
import json

def get_filter_key(key, filter2field):
	_, name, match_strategy = key[2:].split('-')
	if filter2field:
		name = filter2field.get(name, name)

	if match_strategy == 'equal':
		return name
	elif match_strategy == 'contain':
		return '%s__icontains' % name
	elif match_strategy == 'gte':
		return '%s__gte' % name
	elif match_strategy == 'lte':
		return '%s__lte' % name
	elif match_strategy == 'range':
		return '%s__range' % name
	else:
		return name

def get_filter_value(key, filter_options):
	_, _, match_strategy = key[2:].split('-')
	if match_strategy == 'range':
		value = json.loads(filter_options[key])
		return tuple(value)
	else:
		return filter_options[key]

def filter_query_set(query_set, filter_options, filter2field=None):
	if hasattr(filter_options, 'GET'):
		#filter_options是一个request对象
		filter_options = filter_options.GET

	if not filter_options:
		filters = None
	else:
		filters = dict([(get_filter_key(key, filter2field), get_filter_value(key, filter_options)) for key in filter_options if key.startswith('__f-')])

	if not filters:
		return query_set
	return query_set.filter(**filters)
