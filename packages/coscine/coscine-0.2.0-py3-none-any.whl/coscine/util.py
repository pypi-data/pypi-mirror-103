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

import os

###############################################################################
# File read utility function
###############################################################################
# path: Path to the file to read
# Returns: The file contents of the file at $path as byte array
###############################################################################

def fread(path):
	fd = open(path, "rb")
	data = fd.read()
	fd.close()
	return(data)

###############################################################################
# File write utility function
###############################################################################
# path: Path to the file to write
# data: The data to write to the file at $path as byte array
###############################################################################

def fwrite(path, data):
	fd = open(path, "wb")
	data = fd.write(data)
	fd.close()