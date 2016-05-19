# -*- coding: utf-8 -*-
import logging

from outline import models as outline_models

def clean():
	logging.info('clean database for outline app')
	outline_models.ProductModel.objects.all().delete()
	outline_models.Product.objects.all().delete()
