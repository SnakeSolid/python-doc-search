#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask.views

import util


class SearchResult(flask.views.MethodView):
	methods = ["GET"]
	
	def __init__(self, indexer):
		self.indexer = indexer
	
	def get(self):
		query = flask.request.args.get("q")
		
		if query == None or query == "":
			return flask.redirect(flask.url_for("main"))

		pagesize = flask.session["pagesize"] if "pagesize" in flask.session else 10
		page = util.str_to_int(flask.request.args.get("p"), default=1, min_value=1) 
		suggest, maybe = self.indexer.suggest(query)
		result = self.indexer.search(query, page, pagesize)
		target = flask.session["target"] if "target" in flask.session else "blank"
		
		return flask.render_template("search.html", text=query, suggest=suggest, maybe=maybe, result=result, page=page, target=target)
