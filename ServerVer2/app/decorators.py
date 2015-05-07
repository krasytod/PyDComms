#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  decorators.py
#  
#  Copyright 2015 krasytod <krasytod@krasytod-desktop>
#  
from threading import Thread

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper



