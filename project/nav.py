# -*- coding: utf-8 -*-
__author__ = 'robert'

import copy

REQUIREMENT_SECOND_NAVS = [{
	'name': 'project-rd-requirements',
	'displayName': '用户故事',
	'href': '/project/requirements/'
}, {
	'name': 'project-project-requirements',
	'displayName': '产品需求',
	'href': '/project/project_requirements/'
}, {
	'name': 'project-business-requirements',
	'displayName': '业务需求',
	'href': '/project/business_requirements/'
}]

def get_requirement_second_navs(project_id):
	navs = copy.deepcopy(REQUIREMENT_SECOND_NAVS)
	for nav in navs:
		nav['href'] = nav['href'] + (u'?project_id=%s' % project_id)
	return navs