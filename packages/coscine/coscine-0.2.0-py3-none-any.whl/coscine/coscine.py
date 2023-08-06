#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Coscine REST API Python 3.x Wrapper
# Version 0.2.0
# Copyright (c) 2018-2021 RWTH Aachen University
# Contact: coscine@itc.rwth-aachen.de
# Git: https://git.rwth-aachen.de/coscine/docs/public/wiki/-/tree/master/
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

import os
import json
import urllib
import requests
from .metadata import *
from .profile import *
from .util import *

###############################################################################
# 
###############################################################################

class Coscine:

	# Request headers
	_headers = None

	# Language preset
	_lang = None

###############################################################################
# 
###############################################################################

	def __init__(self, token, lang="en"):
		self._lang = lang
		self._headers = {
			"Authorization": "Bearer " + token
		}

###############################################################################
# 
###############################################################################

	@staticmethod
	def _uri(api, endpoint, *args):
		API =	"https://coscine.rwth-aachen.de/coscine/api/" \
			"Coscine.Api.%s/%s"
		uri = API % (api, endpoint)
		if len(args) > 0:
			for arg in args:
				uri += "/" + urllib.parse.quote(arg, safe='')
		return uri

###############################################################################
# 
###############################################################################

	def _get(self, uri):
		response = requests.get(
			uri,
			headers = self._headers,
			verify = True
		)

		if response.ok:
			return response.json()
		else:
			response.raise_for_status()

###############################################################################
# 
###############################################################################

	def _put(self, uri, data):
		response = requests.put(
			uri,
			headers = self._headers,
			verify = True,
			data = data
		)

		if not response.ok:
			response.raise_for_status()

###############################################################################
# 
###############################################################################

	def _download(self, uri):
		response = requests.get(
			uri,
			headers = self._headers,
			verify = True
		)

		if response.ok:
			return response.content
		else:
			response.raise_for_status()

###############################################################################
# 
###############################################################################

	def _delete(self, uri):
		response = requests.delete(
			uri,
			headers = self._headers,
			verify = True
		)

		if not response.ok:
			response.raise_for_status()

###############################################################################
# Get a list of projects matching certain search criteria
###############################################################################

	def get_projects(self):
		uri = self._uri("Project", "Project")
		return self._get(uri)

###############################################################################
# Get a specific project by specifying certain search criteria
###############################################################################

	def get_project(self, displayName):
		for project in self.get_projects():
			if project["displayName"] == displayName:
				return project
		return None

###############################################################################
# Delete a project
###############################################################################

	def delete_project(self, project):
		uri = self._uri("Project", "Project", project["id"])
		self._delete(uri)

###############################################################################
# 
###############################################################################

	def get_subprojects(self, project):
		uri = self._uri("Project", "Subproject", project["id"])
		return self._get(uri)

###############################################################################
# 
###############################################################################

	def get_subproject(self, project, displayName):
		for project in self.get_subprojects():
			if project["displayName"] == displayName:
				return project
		return None

###############################################################################
# 
###############################################################################

	def get_resources(self, project):
		uri = self._uri("Project", "Project",
				project["id"], "resources")
		return self._get(uri)

###############################################################################
# 
###############################################################################

	def get_resource(self, project, displayName):
		for resource in self.get_resources(project):
			if resource["displayName"] == displayName:
				return resource
		return None

###############################################################################
# 
###############################################################################

#	def create_resource(self, project):
#		None

###############################################################################
# 
###############################################################################

	def delete_resource(self, resource):
		uri = self._uri("Resource", "Resource", resource["id"])
		self._delete(uri)

###############################################################################
# 
###############################################################################

	def get_quota(self, resource):
		uri = self._uri("Blob", "Blob", resource["id"], "quota")
		data = self._get(uri)
		quota = int(data["data"]["usedSizeByte"])
		return quota

###############################################################################
# 
###############################################################################

	def get_profile(self, resource):
		uri = self._uri("Metadata", "Metadata", "profiles",
			resource["applicationProfile"], resource["id"])
		return self._get(uri)

###############################################################################
# 
###############################################################################

	def get_vocabularies(self, project, profile):
		vocabularies = {}
		for entry in ApplicationProfile.classes(profile, self._lang):
			uri = self._uri("Metadata", "Metadata", "instances",
					project["id"], entry["class"])
			instance = self._get(uri)
			name = entry["name"]
			vocabularies[name] = ApplicationProfile.vocabulary(
				instance, self._lang
			)
		return vocabularies

###############################################################################
# 
###############################################################################

	def get_template(self, project, resource):
		profile = self.get_profile(resource)
		vocabularies = self.get_vocabularies(project, profile)
		template = Metadata(profile, vocabularies, self._lang)
		return template

###############################################################################
# Get a list of files
###############################################################################

	def list_files(self, resource):
		list = []
		uri = self._uri("Tree", "Tree", resource["id"])
		data = self._get(uri)
		for entry in data["data"]["fileStorage"]:
			obj = {
				"Name": entry["Name"],
				"Path": entry["Path"],
				"Size": entry["Size"],
				"Type": entry["Kind"],
				"Provider": entry["Provider"]
			}
			list.append(obj)
		return list

###############################################################################
# 
###############################################################################

	def upload_file(self, resource, path, data, metadata):
		uri = self._uri("Blob", "Blob", resource["id"], path)
		self.upload_metadata(resource, path, metadata)
		self._put(uri, data)

###############################################################################
# 
###############################################################################

	def upload_metadata(self, resource, path, metadata):
		uri = self._uri("Tree", "Tree", resource["id"], path)
		if isinstance(metadata, Metadata):
			metadata = metadata.generate()
		metatext = json.dumps(metadata)
		self._put(uri, metatext)

###############################################################################
# 
###############################################################################

	def download_file(self, resource, path):
		uri = self._uri("Blob", "Blob", resource["id"], path)
		return self._download(uri)

###############################################################################
# 
###############################################################################

	def download_metadata(self, resource, path):
		uri = self._uri("Tree", "Tree", resource["id"], path)
		return self._get(uri)

###############################################################################
# Download all files of a resource
###############################################################################

	def download_resource(self, resource, path="./"):
		basepath = os.path.join(path, resource["displayName"])
		if not os.path.isdir(basepath):
			os.mkdir(basepath)
		for file in self.list_files(resource):
			filepath = file["Path"].strip("/")
			path = os.path.join(basepath, filepath)
			data = self.download_file(resource, filepath)
			fwrite(path, data)

###############################################################################
# Download all resources of a project
###############################################################################

	def download_project(self, project, path="./"):
		path = os.path.join(path, project["displayName"])
		if not os.path.isdir(path):
			os.mkdir(path)
		for resource in self.get_resources(project):
			self.download_resource(resource, path=path)

###############################################################################
# 
###############################################################################

	def delete_file(self, resource, path):
		uri = self._uri("Blob", "Blob", resource["id"], path)
		self._delete(uri)