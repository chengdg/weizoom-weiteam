# -*- coding: utf-8 -*-

import upyun
import urllib2


BUCKETNAME = None
USERNAME = 'weizoom'
PASSWORD = 'weizoom_weapp'

def set_mode(mode):
	global BUCKETNAME
	if mode == 'development':
		BUCKETNAME = 'testweapp'
	else:
		BUCKETNAME = 'weappimg'

# file_list = dict()
# # -----------------------------------------------
# image_path = "http://%s.b0.upaiyun.com%s"
# def upload_image_to_upyun(file_path, upyun_path):
# 	if settings.MODE == 'develop':
# 		return '/static%s' % upyun_path
		
# 	up = upyun.UpYun(BUCKETNAME, USERNAME, PASSWORD, timeout=300,
# 			endpoint=upyun.ED_AUTO)
# 	#headers = {"x-gmkerl-rotate": "180"}
# 	try:
# 		with open(file_path, 'rb') as f:
# 			try:
# 				res = up.put(upyun_path, f)
# 			except:
# 				res = up.put(upyun_path, f)
			
# 			return image_path % (BUCKETNAME, upyun_path)
# 	except:
# 		notify_message = u"upload_image_to_upyun error {}".format(unicode_full_stack())
# 		watchdog_error(notify_message)
# 		return '/static%s' % upyun_path
# 	return None

def upload_static_file(file_path, upyun_path, check_exist=False):
	up = upyun.UpYun('weappstatic', USERNAME, PASSWORD, timeout=300, endpoint=upyun.ED_AUTO)

	if check_exist:
		path_index = upyun_path.rfind('/')
		temp_path = upyun_path[:path_index]
		if not temp_path in file_list:
			res = up.getlist(temp_path)
			file_list[temp_path] = res
		res = file_list[temp_path]
		for upfile in res:
			if upfile['name'] == upyun_path[path_index+1:]:
				print '[upyun] exist file don\'t need to upload file_path', upyun_path
				return

	print '[upyun] upload local file `%s` to upyun `%s`' % (file_path, upyun_path)
	with open(file_path, 'rb') as f:
		try:
			res = up.put(upyun_path, f)
		except:
			res = up.put(upyun_path, f)
		
		return "http://weappstatic.b0.upaiyun.com%s" % upyun_path