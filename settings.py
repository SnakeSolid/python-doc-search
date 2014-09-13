#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask.views

import util


class SearchSettings(flask.views.MethodView):
	methods = ["GET", "POST"]
	
	def get(self):
		pagesize = flask.session["pagesize"] if "pagesize" in flask.session else 10
		target = flask.session["target"] if "target" in flask.session else "blank"
		
		return flask.render_template("settings.html", pagesize=pagesize, target=target)
	
	def post(self):
		pagesize = util.str_to_int(flask.request.form.get("pagesize"), default=10, min_value=10, max_value=100)
		target = util.str_one_of(flask.request.form.get("target"), "blank", [ "self", "blank" ])
		
		flask.session["pagesize"] = pagesize
		flask.session["target"] = target
		
		return flask.redirect(flask.url_for("main"))
