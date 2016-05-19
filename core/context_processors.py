# -*- coding: utf-8 -*-

from django.conf import settings

#===============================================================================
# top_navs : 获得top nav集合
#===============================================================================
def top_navs(request):
	top_navs = [{
		'name': 'outline',
		'displayName': '数据概况',
		'icon': 'list-alt',
		'href': '/outline/datas/'
	}, {
		'name': 'card',
		'displayName': '微众卡',
		'icon': 'credit-card',
		'href': '#'
	}, {
		'name': 'config',
		'displayName': '配置',
		'icon': 'cog',
		'href': '#'
	}]
	return {'top_navs': top_navs}


def webpack_bundle_js(request):
	return {
		'webpack_bundle_js': settings.WEBPACK_BUNDLE_JS
	}