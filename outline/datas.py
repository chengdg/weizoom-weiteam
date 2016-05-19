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
from core import paginator
from util import db_util
import nav
import models

FIRST_NAV = 'outline'
SECOND_NAV = 'outline-product'

COUNT_PER_PAGE = 50

filter2field = {
	'promotion_finish_date': 'promotion_finish_time'
}

class Datas(resource.Resource):
	app = 'outline'
	resource = 'datas'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		
		return render_to_response('outline/datas.html', c)

	@login_required
	def api_get(request):
		#获取业务数据
		cur_page = request.GET.get('page', 1)
		products = models.Product.objects.filter(owner=request.user)
		products = db_util.filter_query_set(products, request, filter2field)
		products = products.order_by('-id')
		pageinfo, products = paginator.paginate(products, cur_page, COUNT_PER_PAGE)

		product_ids = [product.id for product in products]
		for product in products:
			product.models = []
		id2product = dict([(product.id, product) for product in products])

		product_models = list(models.ProductModel.objects.filter(product_id__in=product_ids))
		for product_model in product_models:
			id2product[product_model.product_id].models.append({
				'id': product_model.id,
				'name': product_model.name,
				'stocks': product_model.stocks
			})

		#组装数据
		rows = []
		for product in products:
			rows.append({
				'id': product.id,
				'name': product.name,
				'weight': product.weight,
				'price': product.price,
				'comment': product.comment,
				'models': product.models,
				'created_at': product.created_at.strftime('%Y-%m-%d %H:%M'),
				'promotion_finish_time': product.promotion_finish_time.strftime('%Y-%m-%d %H:%M:%S')
			})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()
