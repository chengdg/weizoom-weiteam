# -*- coding: utf-8 -*-
import logging

from django.db.models import Q

from project.models import *

def clean():
	Project.objects.filter(~Q(name='default_project')).delete()
