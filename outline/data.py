# -*- coding: utf-8 -*-
import json
import time
import base64

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import nav
import models
from resource import models as resource_models
from util import string_util

FIRST_NAV = 'outline'
SECOND_NAV = 'outline-product'


class Data(resource.Resource):
	app = 'outline'
	resource = 'data'
	
	@login_required
	def get(request):
		#获取业务数据
		product_id = request.GET.get('id', None)
		jsons = {'items':[]}
		if product_id:
			product = models.Product.objects.get(owner=request.user, id=product_id)
			product_data = {
				'id': product.id,
				'name': product.name,
				'weight': product.weight,
				'price': product.price,
				'is_join_promotion': product.is_join_promotion,
				'promotion_finish_date': product.promotion_finish_time.strftime('%Y-%m-%d %H:%M'),
				'channels': product.channels,
				'detail': string_util.raw_html(product.detail),
				'models': [],
				'images': [],
				'documents': [],
				'created_at': product.created_at.strftime('%Y-%m-%d %H:%M')
			}
	
			#获取商品规格
			product_models = models.ProductModel.objects.filter(product_id=product_id)
			for product_model in product_models:
				product_data['models'].append({
					'id': product_model.id,
					'name': product_model.name,
					'stocks': product_model.stocks
				})

			#获取商品图片
			product_image_ids = [product_image.image_id for product_image in models.ProductImage.objects.filter(product_id=product_id)]
			for image in resource_models.Image.objects.filter(id__in=product_image_ids):
				product_data['images'].append({
					'id': image.id,
					'path': image.path
				})

			#获取商品文档
			product_document_ids = [product_document.document_id for product_document in models.ProductDocument.objects.filter(product_id=product_id)]
			for document in resource_models.Document.objects.filter(id__in=product_document_ids):
				product_data['documents'].append({
					'id': document.id,
					'type': document.type,
					'name': document.filename,
					'path': document.path
				})

			jsons['items'].append(('product', json.dumps(product_data)))
		else:
			jsons['items'].append(('product', json.dumps(None)))

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons
		})
		
		return render_to_response('outline/data.html', c)

	@login_required
	def api_put(request):
		product = models.Product.objects.create(
			owner = request.user, 
			name = request.POST['name'], 
			weight = request.POST['weight'], 
			price = request.POST['price'],
			channels = request.POST['channels'],
			detail = request.POST['detail'],
			is_join_promotion = (request.POST['is_join_promotion'] == '1'),
			promotion_finish_time = request.POST['promotion_finish_date']
		)

		product_models = json.loads(request.POST['models'])
		for product_model in product_models:
			models.ProductModel.objects.create(product=product, name=product_model['name'], stocks=product_model['stocks'])

		product_images = json.loads(request.POST['images'])
		for product_image in product_images:
			models.ProductImage.objects.create(product=product, image_id=product_image['id'])

		product_documents = json.loads(request.POST['documents'])
		for product_document in product_documents:
			models.ProductDocument.objects.create(product=product, document_id=product_document['id'])

		response = create_response(200)

		return response.get_response()

	@login_required
	def api_post(request):
		#更新商品
		models.Product.objects.filter(owner=request.user, id=request.POST['id']).update(
			name = request.POST['name'],
			weight = request.POST['weight'],
			price = request.POST['price'],
			channels = request.POST['channels'],
			detail = request.POST['detail'],
			is_join_promotion = (request.POST['is_join_promotion'] == '1'),
			promotion_finish_time = request.POST['promotion_finish_date']
		)

		#删除、重建商品规格
		product = models.Product.objects.get(owner=request.user, id=request.POST['id'])
		models.ProductModel.objects.filter(product_id=product.id).delete()
		product_models = json.loads(request.POST['models'])
		for product_model in product_models:
			models.ProductModel.objects.create(product=product, name=product_model['name'], stocks=product_model['stocks'])

		#删除、重建商品图片
		models.ProductImage.objects.filter(product_id=product.id).delete()
		product_images = json.loads(request.POST['images'])
		for product_image in product_images:
			models.ProductImage.objects.create(product=product, image_id=product_image['id'])

		#删除、重建商品文档
		models.ProductDocument.objects.filter(product_id=product.id).delete()
		product_documents = json.loads(request.POST['documents'])
		for product_document in product_documents:
			models.ProductDocument.objects.create(product=product, document_id=product_document['id'])

		response = create_response(200)

		return response.get_response()

	@login_required
	def api_delete(request):
		models.Product.objects.filter(owner=request.user, id=request.POST['id']).delete()

		response = create_response(200)

		return response.get_response()