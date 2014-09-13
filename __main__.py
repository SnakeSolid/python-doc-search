#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask.views

import config
import indexer
import util


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
		
		if query == None or query == "":
			return flask.redirect(flask.url_for("main"))

		pagesize = flask.session["pagesize"] if "pagesize" in flask.session else 10
		page = util.str_to_int(flask.request.args.get("p"), default=1, min_value=1) 
		suggest, maybe = self.indexer.suggest(query)
		result = self.indexer.search(query, page, pagesize)
		target = flask.session["target"] if "target" in flask.session else "blank"
		
		return flask.render_template("search.html", text=query, suggest=suggest, maybe=maybe, result=result, page=page, target=target)


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


class DocumentView(flask.views.MethodView):
	methods = ["GET"]
	
	def __init__(self, docs_dir):
		self.docs_dir = docs_dir
	
	def get(self, path):
		return flask.send_file(path)


if __name__ == "__main__":
	indexer = indexer.Indexer(config.INDEX_DIR, config.DOC_DIRS)
	
	app = flask.Flask(__name__)
	app.secret_key = config.SECRET_KEY
	
	app.add_url_rule("/", view_func=Main.as_view("main"))
	app.add_url_rule("/search", view_func=SearchResult.as_view("search", indexer))
	app.add_url_rule("/settings", view_func=SearchSettings.as_view("settings"))
	
	for directory in config.DOC_DIRS:
		app.add_url_rule("/{0}/<path:path>".format(directory), view_func=DocumentView.as_view(directory, directory))
		
	app.run("localhost", 8080, True)
