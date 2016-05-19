import os
import sys

def replace_service_name_for(file_name):
	content = None
	with open(file_name, 'rb') as f:
		service_name = sys.argv[1]
		content = f.read()
		content = content.replace('#service_name#', service_name)

	with open(file_name, 'wb') as f:
		f.write(content)

replace_service_name_for('./README.md')