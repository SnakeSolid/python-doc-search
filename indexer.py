#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import os

import bs4
import whoosh.fields
import whoosh.index 
import whoosh.qparser
import whoosh.lang.porter


class Indexer(object):
	def __init__(self, index_dir, docs_dir):
		self.schema = whoosh.fields.Schema(
				path=whoosh.fields.ID(stored=True),
				title=whoosh.fields.TEXT(phrase=False, stored=True),
				content=whoosh.fields.TEXT(stored=True, spelling=True),
				tags=whoosh.fields.KEYWORD(stored=True, lowercase=True, commas=True)
			)
		
		if not os.path.exists(index_dir):
			os.mkdir(index_dir)
			
			self.index = whoosh.index.create_in(index_dir, self.schema)
			
			writer = self.index.writer()
			self.index_recursive(writer, re.compile("\\s+", re.MULTILINE | re.UNICODE), [], docs_dir)
			writer.commit()
		else:
			self.index = whoosh.index.open_dir(index_dir, schema=self.schema)
			
		self.searcher = self.index.searcher()


	def index_recursive(self, writer, regex, tags, docs_dir):
		logging.info("recurcive processing %s (%s)" % (docs_dir, ",".join(tags)))
				
		files = os.listdir(docs_dir)
		
		for filename in files:
			filepath = os.path.join(docs_dir, filename)
			
			if os.path.isdir(filepath):
				self.index_recursive(writer, regex, tags + [ filename ], filepath)
			elif os.path.isfile(filepath) and filename.endswith(".html"):
				logging.info("indexing %s" % (filepath))
				
				with open(filepath, "r") as content:
					soup = bs4.BeautifulSoup(content.read())
					body = soup.body
					
					if body == None:
						continue
					
					content = re.sub(regex, " ", body.get_text().strip())
					
					if content == "":
						continue
					
					path = unicode(filepath)
					title = None
					
					if soup.title != None:
						title = soup.title.get_text()

					if title == None or title == "":
						for header in [ "h1", "h2", "h3", "h4", "h5", "h6" ]:
							if title == None or title == "":
								element = body.find(header)
								
								if element != None:
									title = element.get_text()
								
									break

					if title == None or title == "":
						title = unicode(filename)

					utags = unicode(",".join(tags))
					writer.add_document(path=path, title=title, content=content, tags=utags)
		
	def suggest(self, query):
		qp = whoosh.qparser.QueryParser("content", self.schema)
		q = qp.parse(query)
		
		resultterms = []
		resultsame = False
		
		for field, term in q.all_terms():
			suggests = self.searcher.suggest(field, term, limit=1)
			
			if len(suggests) == 0:
				resultterms.append(term)
			else:
				suggestion = suggests[0]
				
				if whoosh.lang.porter.stem(suggestion) == whoosh.lang.porter.stem(term):
					resultterms.append(term)
				else:
					resultterms.append(suggestion)
					
					resultsame = True
		
		return resultsame, " ".join(resultterms)
		
	def search(self, query, page=1, pagelen=10):
		result = []
		
		parser = whoosh.qparser.MultifieldParser(["title", "content", "tags"], self.schema)
		parser.add_plugin(whoosh.qparser.FuzzyTermPlugin())
		parser.add_plugin(whoosh.qparser.PlusMinusPlugin())
		
		for hit in self.searcher.search_page(parser.parse(query), pagenum=page, pagelen=pagelen):
			result.append({
					"rank": hit.rank,
					"score": hit.score,
					"path": hit["path"],
					"title": hit["title"] if "title" in hit else "",
					"content": hit.highlights("content"),
					"tags": hit["tags"]
				})
			
		return result
