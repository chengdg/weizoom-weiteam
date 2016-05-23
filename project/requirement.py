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
from business.project.b_project import BProject
from business.project.b_project_repository import BProjectRepository


class Requirement(resource.Resource):
	app = 'project'
	resource = 'requirement'
	
	@login_required
	def api_put(request):
		project_id = request.POST['project_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)
		b_project.add_requirement({
			"owner": request.user,
			"title": request.POST['title'],
			"importance": request.POST['importance'],
			"content": request.POST['content']
		})
		
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
		project_id = request.POST['project_id']
		requirement_id = request.POST['requirement_id']
		b_project = BProjectRepository.get().get_project_by_id(project_id)
		b_project.delete_requirement(requirement_id)

		response = create_response(200)
		return response.get_response()