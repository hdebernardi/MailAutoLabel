#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import sys         # exit
#import email       # email representation
#import chardet     # detect encoding
#import bs4         # html decoding

import logging
import sys
import re
import email
import imaplib

from email.parser import HeaderParser

logger = logging.getLogger()

class IMAP_Message:
	def __init__(self, connection, **kwargs):
		self.connection = connection
		self.kwargs = kwargs

		#self._uid_list = self._query_uids(**kwargs)
	"""
	def _query_uids(self, **kwargs):
		#query = IMAP_Query(kwargs)
		status, uids = self.connection.search(None, query)
	"""
	def _get_uids(self, folder):
		"""Get all the messages' identifiants from a folder.
		TODO
		"""
		logger.info('Searching for ids.')
		status, messages_ids = self.connection.search(None, 'ALL')
		return messages_ids[0].split() if messages_ids[0] is not None else []