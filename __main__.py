#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask.views

import config
import indexer


class Main(flask.views.MethodView):
	methods = ["GET"]
	
	def get(self):
		return flask.render_template("index.html")


class SearchResult(flask.views.MethodView):
	methods = ["GET"]
	
	def __init__(self, indexer):
		self.indexer = indexer
	
	def get(self):
		query = flask.request.args.get("q")
		rawpage = flask.request.args.get("p")
		
		if query == None or query == "":
			return flask.redirect(flask.url_for("main"))

		if rawpage == None:
			page = 1
		else:
			try:
				page = int(rawpage)
			except ValueError:
				page = 0
		
		if page < 1:
			page = 1
		
		suggest, maybe = self.indexer.suggest(query)
		result = self.indexer.search(query, page)
		
		return flask.render_template("search.html", text=query, suggest=suggest, maybe=maybe, result=result, page=page)


class DocumentView(flask.views.MethodView):
	methods = ["GET"]
	
	def __init__(self, docs_dir):
		self.docs_dir = docs_dir
	
	def get(self, path):
		return flask.send_file(path)


if __name__ == "__main__":
	indexer = indexer.Indexer(config.INDEX_DIR, config.DOC_DIRS)
	
	app = flask.Flask(__name__)
	app.add_url_rule("/", view_func=Main.as_view("main"))
	app.add_url_rule("/search", view_func=SearchResult.as_view("search", indexer))
	
	for directory in config.DOC_DIRS:
		app.add_url_rule("/{0}/<path:path>".format(directory), view_func=DocumentView.as_view(directory, directory))
		
	app.run("localhost", 8080, False)
