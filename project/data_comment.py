# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import nav
import models


class DataComment(resource.Resource):
	app = 'outline'
	resource = 'data_comment'
	

	@login_required
	def api_post(request):
		product_id = request.POST['product_id']
		comment = request.POST['comment']

		models.Product.objects.filter(owner=request.user, id=product_id).update(comment=comment)

		response = create_response(200)

		return response.get_response()