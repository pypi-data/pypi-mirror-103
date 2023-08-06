#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Coscine REST API Python 3.x Wrapper
# Version 0.2.0
# Copyright (c) 2018-2021 RWTH Aachen University
# Contact: coscine@itc.rwth-aachen.de
# Support: servicedesk@rwth-aachen.de
# https://git.rwth-aachen.de/coscine/docs/public/wiki/-/tree/master/
# Please direct bug reports, feature requests or questions at the URL above
# by opening an issue.
###############################################################################
# This python wrapper implements a client for the Coscine API.
# Coscine is an open source project at RWTH Aachen University for
# the management of research data.
# Visit https://coscine.rwth-aachen.de for more information.
###############################################################################
# MIT License
#
# Copyright (c) 2018-2021 RWTH Aachen University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
###############################################################################

###############################################################################
#
###############################################################################

class ApplicationProfile:

###############################################################################
#
###############################################################################

	@staticmethod
	def entries(profile):
		return profile[0]["@graph"]

###############################################################################
#
###############################################################################

	@staticmethod
	def get_name(entry, lang):
		field = ApplicationProfile.get_field(entry, "name")
		if field:
			for names in field:
				if names["@language"] == lang:
					return names["@value"]
		return None

###############################################################################
#
###############################################################################

	@staticmethod
	def get_field(entry, name):
		SHACL = "http://www.w3.org/ns/shacl#%s"
		identifier = SHACL % name
		if identifier in entry:
			return entry[identifier]
		else:
			return None

###############################################################################
#
###############################################################################

	@staticmethod
	def get_value(entry, name):
		field = ApplicationProfile.get_field(entry, name)
		if field:
			return field[0]["@id"]
		else:
			return None

###############################################################################
#
###############################################################################

	@staticmethod
	def classes(profile, lang):
		classes = []
		for entry in ApplicationProfile.entries(profile):
			value = ApplicationProfile.get_value(entry, "class")
			if value:
				name = ApplicationProfile.get_name(entry, lang)
				classes.append({
					"name": name,
					"class": value
				})
		return classes

###############################################################################
#
###############################################################################

	@staticmethod
	def vocabulary(instance, lang):
		vocabulary = {}
		if not lang in instance or len(instance[lang]) == 0:
			lang = "en"
		for entry in instance[lang]:
			vocabulary[entry["name"]] = entry["value"]
		return vocabulary

###############################################################################
#
###############################################################################

	@staticmethod
	def default_value(entry):
		IDENTIFIER = "https://purl.org/coscine/fixedValue"
		if IDENTIFIER in entry:
			return entry[IDENTIFIER][0]["@id"]
		else:
			return None

###############################################################################
#
###############################################################################

	@staticmethod
	def is_required(entry):
		minCount = ApplicationProfile.get_field(entry, "minCount")
		if minCount and int(minCount[0]["@value"]) > 0:
			return True
		else:
			return False