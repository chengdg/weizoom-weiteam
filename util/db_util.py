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

def get_filter_value(key, request):
	_, _, match_strategy = key[2:].split('-')
	if match_strategy == 'range':
		value = json.loads(request.GET[key])
		return tuple(value)
	else:
		return request.GET[key]

def filter_query_set(query_set, request, filter2field):
	filters = dict([(get_filter_key(key, filter2field), get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
	print '-*-' * 20
	print filters
	print '-*-' * 20

	if not filters:
		print 'return directly'
		return query_set
	return query_set.filter(**filters)
