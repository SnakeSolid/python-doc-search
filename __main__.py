#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask

import config
import indexer
import main
import search
import settings
import static


if __name__ == "__main__":
	indexer = indexer.Indexer(config.INDEX_DIR, config.DOC_DIRS)
	
	app = flask.Flask(__name__)
	app.secret_key = config.SECRET_KEY
	
	app.add_url_rule("/", view_func=main.Main.as_view("main"))
	app.add_url_rule("/search", view_func=search.SearchResult.as_view("search", indexer))
	app.add_url_rule("/settings", view_func=settings.SearchSettings.as_view("settings"))
	
	for directory in config.DOC_DIRS:
		app.add_url_rule("/{0}/<path:path>".format(directory), view_func=static.DocumentView.as_view(directory, directory))
		
	app.run("localhost", 8080, False)
