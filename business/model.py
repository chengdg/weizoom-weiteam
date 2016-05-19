# -*- coding: utf-8 -*-
import logging

class Model(object):
	"""
	领域业务对象的基类
	"""
	__slots__ = ('context', )
	
	def __init__(self):
		self.context = {}

		for slot in self.__slots__:
			#logging.info("setting '%s'" % slot)
			setattr(self, slot, None)

	def _init_slot_from_model(self, model, slots=None):
		if not slots:
			slots = self.__slots__
			
		for slot in slots:
			value = getattr(model, slot, None)
			if value != None:
				if 'id' == slot:
					value = int(value)
				setattr(self, slot, value)

	def after_from_dict(self):
		"""
		from_dict调用结束前的hook函数，允许sub class修改from_dict的结果
		"""
		pass

	@classmethod
	def from_dict(cls, dict, slots=None):
		instance = cls()
		if not slots:
			slots = cls.__slots__

		for slot in slots:
			value = dict.get(slot, None)

			setattr(instance, slot, value)
		instance.after_from_dict()
		return instance

	def to_dict(self, *extras, **kwargs):
		result = dict()
		if kwargs and 'slots' in kwargs:
			slots = kwargs['slots']
		else:
			slots = self.__slots__

		for slot in slots:
			result[slot] = getattr(self, slot, None)

		if extras:
			for item in extras:
				result[item] = getattr(self, item, None)
			
		return result


class Service(object):
	"""
	领域服务的基类
	"""
	__slots__ = ('context', )

	@classmethod
	def get(cls, webapp_owner=None, webapp_user=None):
		return cls(webapp_owner, webapp_user)
	
	def __init__(self, webapp_owner=None, webapp_user=None):
		self.context = {
			'webapp_user': webapp_user,
			'webapp_owner': webapp_owner
		}
