# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models as auth_models

import business.model as business_model
from business.decorator import cached_context_property
from requirement import models as requirement_models
from account import models as account_models
from business.account.b_user_repository import BUserRepository

class BRequirementComment(business_model.Model):
	__slots__ = (
		'id',
		'content',
		'creater',
		'created_at'
	)
	
	@staticmethod
	def from_model(db_model, fill_creater=True):
		requirement = BRequirementComment(db_model, fill_creater)

		return requirement

	def __init__(self, model=None, fill_creater=True):
		business_model.Model.__init__(self)
		self._init_slot_from_model(model)
		self.context['db_model'] = model

		if fill_creater:
			self.creater = BUserRepository.get().get_user(model.creater_id)