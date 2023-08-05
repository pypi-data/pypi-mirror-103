
Changelog
=========

2.1.0 (2020-04-21)
------------------

* Refresh project by adding support for Docker, improving unit tests and freezing dependencies

2.0.0 (2020-05-22)
------------------

* Simplify project by dropping support for all Python versions except for the current version (3.8)
* Add support for repeated pages (e.g. events -> event details)
  
1.4.0 (2020-01-19)
------------------

* Add Python 3.8 support
* Drop Python 3.4 support
* Don't remove output folder, but remove it's contents instead. Removing the
  folder would cause permission issues, when serving with a local web server for development.

1.3.0 (2019-11-27)
------------------

* Add option to render Mako exceptions

1.2.0 (2019-10-18)
------------------

* Set default input encoding to UTF-8

1.1.0 (2019-10-08)
------------------

* Added subdirectory support
* Added support for pretty urls (default)
* Both <PAGE NAME>.template.mako and <PAGE NAME>.part.mako files won't be rendered now

1.0.0 (2019-09-25)
------------------

* Template rendering is working
* Added YAML data file support
* Improved program verbosity

0.1.0 (2019-09-21)
------------------

* Drop support for Python 2
* Implement middlewares

0.0.0 (2019-09-21)
------------------

* First release on PyPI
