#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module consists of an unique function.
Its primary goal is to implement a search query.

See more at : https://tools.ietf.org/html/rfc3501#section-6.4.4
"""

SEARCH_KEY_ALLOWED = {'unseen': 'unseen', 'from' : 'from {}'}

def build_query(**kwargs: dict) -> str:
	"""Build a query with the given kwargs.

	Current supported keys are : 'unseen' and 'from <address>'.
	They should be contained on a dictionnary called search.

	Args:
		kwargs : The search keys.

	Returns:
		The query as a string. ALL is returned if no key matched.
	"""
	query = []
	for value in kwargs.values():
		for key_, value_ in value.items():
			if key_ == 'search':
				for key__, value__ in value_.items():
					if key__ in SEARCH_KEY_ALLOWED:
						query.append(SEARCH_KEY_ALLOWED[key__].format(value__))

	if query:
		return ' '.join(query)

	return 'ALL'
