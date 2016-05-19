# -*- coding: utf-8 -*-
import json
import time
import logging
from datetime import datetime, timedelta

from behave import *
import bdd_util

from outline import models as outline_models

@when(u"{user}添加商品")
def step_impl(context, user):
	context.products = json.loads(context.text)
	for product in context.products:
		if not product.get('models', None):
			product['models'] = "[]"
		else:
			product['models'] = json.dumps(product['models'])

		response = context.client.put('/outline/api/data/', product)
		bdd_util.assert_api_call_success(response)


@when(u"{user}删除商品'{product_name}'")
def step_impl(context, user, product_name):
	user_id = bdd_util.get_user_id_for(user)
	product = outline_models.Product.objects.get(owner_id=user_id, name=product_name)

	response = context.client.delete('/outline/api/data/', {'id': product.id})
	bdd_util.assert_api_call_success(response)


@then(u"{user}能获得商品列表")
def step_impl(context, user):
	expected = json.loads(context.text)

	response = context.client.get('/outline/api/datas/')
	actual = json.loads(response.content)['data']['rows']
	logging.info(actual)
	
	bdd_util.assert_list(expected, actual)