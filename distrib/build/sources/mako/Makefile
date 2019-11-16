# SmoothWall Build system.
#
# (c) SmoothWall Ltd 2005
#
# This code is distributed under the terms of the GPL v2.

include ../Makefile.conf

PACKAGE = Mako
VERSION = 0.7.2

BASE_URL = https://pypi.python.org/packages/source/M/Mako

CONFIGURE = yes

configure: $(DIR)/
	@( \
	  cd $(DIR); \
	  python setup.py build; \
	  python setup.py install; \
	)
	  

include ../Makefile.rules
