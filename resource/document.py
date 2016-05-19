# -*- coding: utf-8 -*-

import json
from datetime import datetime
import os
import random
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.conf import settings

from core import resource
from core.jsonresponse import create_response
import models

suffix2type = {
	'ppt': 'ppt',
	'pptx': 'ppt',
	'doc': 'doc',
	'docx': 'doc',
	'jpg': 'image',
	'gif': 'image',
	'jpeg': 'image',
	'png': 'image',
	'bmp': 'image',
	'pdf': 'pdf',
	'zip': 'rar',
	'rar': 'rar',
	'xls': 'xls',
	'xlsx': 'xls',
	'cvs': 'xls'
}

class Document(resource.Resource):
	"""
	文档
	"""
	app = 'resource'
	resource = 'document'
	def __get_file_name(file_name):
		"""
		基于上传的文件的文件名file_name，生成一个server端唯一的文件名
		"""
		pos = file_name.rfind('.')
		if pos == -1:
			suffix = ''
		else:
			suffix = file_name[pos:]
			
		return suffix2type.get(suffix[1:], 'text'), '%s_%d%s' % (str(time.time()).replace('.', '0'), random.randint(1, 1000), suffix)
	
	@login_required
	def put(request):
		file = request.FILES.get('file', None)

		#读取二进制内容
		content = []
		if file:
			for chunk in file.chunks():
				content.append(chunk)

		#获取存储文件的目录和文件信息
		file_type, file_name = Document.__get_file_name(file.name)
		store_dir = time.strftime('%Y%m%d')
		dir_path = os.path.join(settings.UPLOAD_DIR, store_dir)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		file_path = os.path.join(dir_path, file_name)

		#写文件内容
		dst_file = open(file_path, 'wb')
		print >> dst_file, ''.join(content)
		dst_file.close()

		#保存图片信息到mysql中
		document_path = '/static/upload/%s/%s' % (store_dir, file_name)
		document = models.Document.objects.create(
			filename = file.name,
			type = file_type,
			user = request.user,
			path = document_path
		)

		response = create_response(200)
		response.data = {
			'id': document.id,
			'type': document.type,
			'name': document.filename,
			'path': document_path
		}
		return response.get_response()
