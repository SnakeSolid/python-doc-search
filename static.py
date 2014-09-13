#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask.views


class DocumentView(flask.views.MethodView):
	methods = ["GET"]
	
	def __init__(self, docs_dir):
		self.docs_dir = docs_dir
	
	def get(self, path):
		return flask.send_file(path)
