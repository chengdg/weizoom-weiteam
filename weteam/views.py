# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def about_us(request, webapp_id):
	return render_to_response('weizoom_about.html')