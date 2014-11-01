# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from appconf import AppConf


class CriticalConf(AppConf):
    PHANTOMJS_PATH = 'phantomjs'
    PENTHOUSE_PATH = 'penthouse.js'

    class Meta:
        prefix = 'critical'
