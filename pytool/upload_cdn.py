# -*- coding: utf-8 -*-

import upyun_util
import os

for dir in ['./dist/h5_static/css', './dist/h5_static/js']:
	for f in os.listdir(dir):
		if not '-' in f: 
			#not md5 version, ignore
			continue

		if 'css' in dir:
			upyun_dir = 'css'
		else:
			upyun_dir = 'js'
		upyun_path = '/h5_static/%s/%s' % (upyun_dir, f)
		file_path = os.path.join(dir, f)
		upyun_util.upload_static_file(file_path, upyun_path)
