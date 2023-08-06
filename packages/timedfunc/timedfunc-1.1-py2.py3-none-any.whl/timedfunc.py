#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
"""
    @license
    Copyright (c) Daniel Pauli <dapaulid@gmail.com>

    This source code is licensed under the MIT license found in the
    LICENSE file in the root directory of this source tree.
"""
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# package info
#-------------------------------------------------------------------------------
#
"""Measures execution time of python functions using decorators"""
__version__ = '1.1'

#-------------------------------------------------------------------------------
# default values
#-------------------------------------------------------------------------------
#
tfconfig = {
	"output": ["stderr"],
	"format": "pretty",
	"enabled": True,
}

#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
#
from functools import wraps
from timeit import default_timer as timer
import atexit
import sys
import os

#-------------------------------------------------------------------------------
# variables
#-------------------------------------------------------------------------------
#
timing_stats = []

#-------------------------------------------------------------------------------
# API
#-------------------------------------------------------------------------------
#
def timedfunc(func):
	if not get_param("enabled"):
		# disabled -> act as identity decorator
		return func
	# end if
	timing_stat = Stat(func.__qualname__)
	timing_stats.append(timing_stat)
	@wraps(func)
	def wrapper(*args, **kwargs):
		start_time = timer()
		result = func(*args, **kwargs)
		timing_stat.update(timer() - start_time)
		return result
	return wrapper
# end function


#-------------------------------------------------------------------------------
# helpers
#-------------------------------------------------------------------------------
#
class Stat:
	def __init__(self, name):
		self.name = name
		self.count = 0
		self.sum = 0
		self.min = None
		self.max = None
	# end function

	def update(self, value):
		if self.count > 0:
			self.min = min(self.min, value)
			self.max = max(self.max, value)
		else:
			self.min = value
			self.max = value
		# end if
		self.count += 1
		self.sum += value
	# end function

	def mean(self):
		return self.sum / self.count if self.count > 0 else None
	# end function

# end class

#-------------------------------------------------------------------------------
#
def get_env(name, default):
	if name not in os.environ:
		return default
	# end if
	value = os.environ[name]
	# use same type as default value
	if type(default) is bool:
		# special handling of falsy string values
		return value.lower() not in ['false', 'no', '0']
	elif type(default) is list:
		# special handling for lists
		return value.split(',')
	else:
		# just do the cast
		return type(default)(value)
	# end if
# end function

#-------------------------------------------------------------------------------
#
def get_param(name):
	# check environment variable
	return get_env('TIMEDFUNC_' + name.upper(), tfconfig[name])
# end function

#-------------------------------------------------------------------------------
#
def fmt(time):
	return "%0.3f ms" % time if time is not None else "None"
# end function

#-------------------------------------------------------------------------------
#
def print_stats():
	if not get_param("enabled"):
		# disabled -> do nothing
		return
	# end if

	for output in get_param("output"):
		out = None
		if output == 'stdout':
			out = sys.stdout
		elif output == 'stderr':
			out = sys.stderr
		else:
			out = open(output, 'w')
		# end if

		widths = (30, 8, 12, 12, 12)

		row = " {0: <%d} | {1: >%d} | {2: >%d} | {3: >%d} | {4: >%d}" % widths
		hrule = "+".join('-' * (w + 2) for w in widths)

		out.write(hrule + '\n')
		out.write(row.format("timed functions", "calls", "min", "mean", "max") + '\n')
		out.write(hrule + '\n')
		for stat in timing_stats:
			out.write(row.format(stat.name, stat.count, fmt(stat.min), fmt(stat.mean()), fmt(stat.max)) + '\n')
		# end for
		out.write(hrule + '\n')
		out.flush()
	# end for
# end function

#-------------------------------------------------------------------------------
# entry
#-------------------------------------------------------------------------------
#
atexit.register(print_stats)

#-------------------------------------------------------------------------------
# end of file
