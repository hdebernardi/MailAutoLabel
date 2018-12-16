#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import sys         # exit
#import email       # email representation
#import chardet     # detect encoding
#import bs4         # html decoding

import logging
from mailautolabel.imap.parser import get_rid_of_html

LOGGER = logging.getLogger()

def get_normalized_message(**kwargs):
	"""TODO.
	"""
	flags = kwargs['flags'] or None
	folder = kwargs['folder'] or None
	mail = kwargs['mail'] or None
	header_keys = kwargs['header_keys'] or None

	message = {}

	message['flags'] = flags
	message['folder'] = folder

	if header_keys:
		for key in header_keys:
			message[key] = mail.headers[key]
	else:
		for key in mail.headers.keys():
			message[key] = mail.headers[key]

	if mail.body is not None:
		message['body'] = get_rid_of_html(mail.body)
	else:
		for part in mail.parts:
			if part == 'text/plain':
				message['body'] = get_rid_of_html(part.body)
			elif part == 'text/html':
				message['body'] = get_rid_of_html(part.body)

	return message
