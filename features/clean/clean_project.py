# -*- coding: utf-8 -*-
import logging

from project.models import *

def clean():
	Project.objects.all().delete()
