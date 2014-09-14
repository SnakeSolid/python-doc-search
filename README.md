# Document search

Web application to search any text in HTML files. Tested with Python
2.7.

Source HTML files can be placed in "docs" folder by default (DOC_DIRS
constant). When application starts it check index (INDEX_DIR constant)
directory. If index does not exists it will be created.

Index contains following fields:

 * path - path to HTML file;
 * title - calculated document title (in this order: title text, first
   h1-h6 tag text, file name");
 * content - text content of file (without formatting and line feeds);
 * tags - comma separated parent directory names of file;

### Dependencies

* Flask - web server;
* Beautiful Soup 4 - HTLM parser;
* Whoosh - full text search and highlight;
* Metro UI CSS - metro ui like css styles.

All libraries can be installed with package manager or downloaded from
their official sites.

Full version with libraries available [here](https://bitbucket.org/snakesolid/python-doc-search/downloads/doc-search.tgz).

### License

All source code available under MIT License.
