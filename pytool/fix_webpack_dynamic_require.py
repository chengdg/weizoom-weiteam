# -*- coding: utf-8 -*-

import os

page_file_path = './node_modules/reactman/lib/component/page/Page.react.js'

items = []
src_file = open(page_file_path)
for line in src_file:
	line = line.rstrip()
	if '//for windows cnpm' in line:
		items.append('//' + line)
	elif '//for mac cnpm' in line:
		items.append(line[2:])
	else:
		items.append(line)
content = '\n'.join(items)
src_file.close()

dst_file = open(page_file_path, 'w')
print >> dst_file, content
dst_file.close()
