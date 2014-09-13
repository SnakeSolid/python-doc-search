#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask.views


class Main(flask.views.MethodView):
	methods = ["GET"]
	
	def get(self):
		return flask.render_template("index.html")
