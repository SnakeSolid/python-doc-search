#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys


def str_to_int(text, default=0, min_value=0, max_value=sys.maxint):
    if text != None:
        try:
            result = int(text)
        except ValueError:
            result = default
    else:
        result = default
    
    if result < min_value:
        result = min_value
    
    if result > max_value:
        result = max_value
    
    return result


def str_one_of(text, default, values):
    if text == None:
        return default
    
    if not text in values:
        return default
    
    return text
