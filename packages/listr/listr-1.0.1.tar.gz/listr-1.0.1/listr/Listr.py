#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
python list with pointer
author: Slamet Hidayat
"""

class Listr(object):
	def __init__(self):
		self.list = []
		self.pointer = 0
		self.iter_num = 0
	def import_list(self,l):
		for i in l:
			self.list.append(i)
	def current(self): # get current value
		return self.list[self.pointer]
	def next(self): # move pointer to next and return value
		if self.pointer != len(self.list)-1:
			self.pointer = self.pointer+1
			return self.current()
		else:
			self.start()
			return self.current()
	def prev(self): # move value to previous and return value
		if self.pointer == 0:
			self.end()
		else:
			self.pointer = self.pointer-1
		return self.current()
	def start(self): # move pointer to start and return value
		self.pointer = 0
		return self.current()
	def end(self): # move pointer to end and return value
		self.pointer = len(self.list)-1
		return self.current()
	def iter(self): # iterator
		if self.iter_check():
			current = self.current()
			self.iter_num += 1
			self.next()
			return current
		else:
			return False
	def iter_reset(self): # reset iterator
		self.iter_num = 0
		return True
	def iter_check(self): # iterator check
		if self.iter_num < len(self.list)-1 or self.iter_num == len(self.list)-1:
			return True
		else:
			return False
	def __iter__(self):
		self.iter_reset()
		return self
	
	def __next__(self):
		ret = self.iter()
		if ret != False:
			return ret
		else:
			raise StopIteration
