#!/usr/bin/env python
# -*- coding: utf-8 -*-

class IMAP_Query:
	"""TODO
	"""
	def __init__(self, **kwargs):
		self.kwargs = kwargs

		self.supported = {
			'unseen'
		}

	def build(self):
		query = []

		for key, value in self.kwargs.items():
			if value is not None and key == 'search':
				print(key, value)
				#query.append(self.supported[str(key)].format(value))
				#query.append('{}'.format(value))

		if query:
			return ' '.join(query)

		return 'ALL'