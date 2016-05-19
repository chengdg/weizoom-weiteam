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

class TaskFinishTime(resource.Resource):
	app = 'outline'
	resource = 'task_finish_time'
	
	@login_required
	def api_get(request):
		values = [
			(u"7天", 1), 
			(u"6天", 6), 
			(u"5天", 1), 
			(u"2天", 5), 
			(u"0天", 18)
		]

		info = {
			'title': u'任务完成时间分布-base=%s' % request.GET['base'],
			'data_name': u'完成时间',
			'values': values
		}

		chart = chart_util.create_pie_chart(info)

		response = create_response(200)
		response.data = chart
		return response.get_response()
