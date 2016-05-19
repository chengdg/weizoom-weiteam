# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import nav
from util import date_util
from util import chart_util

today = datetime.today()
def before(delta):
	return today - timedelta(delta)

fans_datas = [
(before(31), 33),
(before(30), 43),
(before(29), 42),
(before(28), 16),
(before(27), 5),
(before(26), 10),
(before(25), 23),
(before(24), 27),
(before(23), 20),
(before(22), 46),
(before(21), 37),
(before(20), 15),
(before(19), 12),
(before(18), 19),
(before(17), 33),
(before(16), 13),
(before(15), 21),
(before(14), 22),
(before(13), 0),
(before(12), 5),
(before(11), 31),
(before(10), 1430),
(before(9), 98),
(before(8), 12),
(before(7), 1),
(before(6), 1),
(before(5), 1),
(before(4), 2),
(before(3), 10),
(before(2), 415),
(before(1), 21),
(today, 0)
]

class FansTrend(resource.Resource):
	app = 'outline'
	resource = 'fans_trend'
	
	@login_required
	def api_get(request):
		today = datetime.today()
		start_date = today - timedelta(30)
		end_date = today + timedelta(1)
		dates = [date.strftime('%m-%d') for date in date_util.get_date_range_list(start_date, end_date)]
		real_dates = date_util.get_date_range_list(start_date, end_date)
		
		#初始化每天对应的数量
		date2count = dict([(date, 0) for date in dates])

		for fans in fans_datas:
			date = fans[0].strftime('%m-%d')
			date2count[date] = fans[1]

		#进行累加
		values = date2count.items()
		values.sort(lambda x,y: cmp(x[0], y[0]))
		total_count = 0
		for date, count in values:
			total_count += count
			date2count[date] = total_count

		values = date2count.items()
		values.sort(lambda x,y: cmp(x[0], y[0]))
		info = {
			'title': u'',
			'data_name': u'粉丝总量',
			'values': values
		}

		chart = chart_util.create_line_chart(info)

		response = create_response(200)
		response.data = chart
		return response.get_response()
