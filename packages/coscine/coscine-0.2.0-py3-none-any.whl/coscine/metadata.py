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
# Dependencies
###############################################################################

from collections.abc import MutableMapping
from .exceptions import *
from .profile import *

###############################################################################
# Coscine Metadata interface
###############################################################################

class Metadata(MutableMapping):

###############################################################################
#
###############################################################################

	def __init__(self, profile, vocabulary, lang="en"):
		self.store = {}
		self.profile = profile
		self.vocabulary = vocabulary
		self._lang = lang
		self.reset()

###############################################################################
#
###############################################################################

	def __getitem__(self, key):
		return self.store[key]["value"]

###############################################################################
#
###############################################################################

	def __setitem__(self, key, value):
		if key not in self.store:
			raise KeyError()
		elif self.store[key]["controlled"]:
			values = self.vocabulary[key]
			if value in values:
				self.store[key]["value"] = values[value]
				self.store[key]["set"] = True
			else:
				raise VocabularyError()
		else:
			self.store[key]["value"] = value
			self.store[key]["set"] = True

###############################################################################
#
###############################################################################

	def __delitem__(self, key):
		del self.store[key]

###############################################################################
#
###############################################################################

	def __iter__(self):
		return iter(self.store)

###############################################################################
#
###############################################################################

	def __len__(self):
		return len(self.store)

###############################################################################
#
###############################################################################

	def __repr__(self):
		text = "--------------------------------------------------\n" \
			"Metadata Template %s\n" % self.profile[0]["@id"]
		text += "--------------------------------------------------\n" \
			"RCFS | KEY        | VALUE\n" \
			"--------------------------------------------------\n"
		mask = "%d%d%d%d | %s = %s\n"
		for field in self.store:
			value = self.store[field]["value"]
			required = self.store[field]["required"]
			controlled = self.store[field]["controlled"]
			fixed = self.store[field]["fixed"]
			set = self.store[field]["set"]
			text += mask % (required, controlled, fixed, set, \
								field, value)
		return text

###############################################################################
#
###############################################################################

	def reset(self):
		self.store.clear()
		for entry in ApplicationProfile.entries(self.profile):
			name = ApplicationProfile.get_name(entry, self._lang)
			if name is not None:
				value = ApplicationProfile.default_value(entry)
				controlled = name in self.vocabulary
				required = ApplicationProfile.is_required(entry)
				path = ApplicationProfile.get_value(entry, "path")
				preset = value is not None
				if controlled:
					type = "uri"
					datatype = ApplicationProfile.get_value(entry, "class")
				else:
					datatype = ApplicationProfile.get_value(entry, "datatype")
					type = "literal"
				self.store[name] = {
					"value": value,
					"controlled": controlled,
					"required": required,
					"path": path,
					"type": type,
					"datatype": datatype,
					"set": preset,
					"fixed": preset
				}

###############################################################################
#
###############################################################################

	def generate(self):
		metadata = {}
		RDFTYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

		# Set metadata application profile
		metadata[RDFTYPE] = [{
			"type": "uri",
			"value": self.profile[0]["@id"]
		}]

		# Collect missing required fields
		missing = []

		# Set metadata fields
		for key in self.store:
			field = self.store[key]
			if field["set"] is False:
				if field["required"]:
					missing.append(key)
				else:
					continue

			path = field["path"]
			metadata[path] = [{
				"value": field["value"],
				"datatype": field["datatype"],
				"type": field["type"]
			}]

		# Check for missing fields
		if len(missing) > 0:
			raise RequirementError(missing)

		return metadata