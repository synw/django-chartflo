# -*- coding: utf-8 -*-

from django.conf import settings


ENGINE = getattr(settings, 'CHARTFLO_ENGINE', "vegalite")
