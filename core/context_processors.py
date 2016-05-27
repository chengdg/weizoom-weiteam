# -*- coding: utf-8 -*-

from django.conf import settings

#===============================================================================
# top_navs : 获得top nav集合
#===============================================================================
def top_navs(request):
	top_navs = None
	if not request.user.is_active:
		return {'top_navs': []}

	if (not '/project/' in request.path) or ('project/projects' in request.path):
		top_navs = [{
			'name': 'project',
			'displayName': '团队看板',
			'icon': 'fa-newspaper-o',
			'href': '/project/projects/'
		}, {
			'name': 'weekly_report',
			'displayName': '周报',
			'icon': 'calendar',
			'href': '/report/weekly_report/'
		}]

		if request.user.username == 'manager':
			top_navs.append({
				'name': 'account',
				'displayName': '成员',
				'icon': 'fa-users',
				'href': '/account/users/'
			})
			top_navs.append({
				'name': 'config',
				'displayName': '配置',
				'icon': 'cog',
				'href': '#'
			})

	else:
		project_id = request.GET['project_id']
		top_navs = [{
			'name': 'kanban',
			'displayName': '看板',
			'icon': 'list-alt',
			'href': '/project/kanban/?project_id='+project_id
		}, {
			'name': 'requirement',
			'displayName': '需求',
			'icon': 'fa-database',
			'href': '/project/requirements/?project_id='+project_id
		}, {
			'name': 'bug',
			'displayName': 'Bug',
			'icon': 'fa-bug',
			'href': '#'
		}, {
			'name': 'statistics',
			'displayName': '统计',
			'icon': 'fa-line-chart',
			'href': '#'
		}, {
			'name': 'member',
			'displayName': '成员',
			'icon': 'fa-users',
			'href': '/project/members/?project_id='+project_id
		}, {
			'name': 'config',
			'displayName': '配置',
			'icon': 'fa-cog',
			'href': '#'
		}]
	return {'top_navs': top_navs}


def webpack_bundle_js(request):
	return {
		'webpack_bundle_js': settings.WEBPACK_BUNDLE_JS
	}