#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger()

from imaplib import IMAP4, IMAP4_SSL

class IMAP_Connection():
	"""A class aimed to implement a simple IMAP connection.

	Args:
		hostname (str): The server's address.
		port (int): The server's port. IMAP uses 143 by default, 993 with SSL.
		ssl (bool): Should we use SSL encryption ? Default is True.
	"""
	def __init__(self, hostname, port=None, ssl=True):
		self.hostname = hostname

		if ssl:
			self.port = port or 993
			self.server = IMAP4_SSL(host=self.hostname, port=self.port)
		else:
			self.port = port or 143
			self.server = IMAP4(host=self.hostname, port=self.port)

		logger.info('IMAP connection initialized for {}:{} {}'.format(
			self.hostname, self.port, 'over SSL.' if ssl else '.'))

	def login(self, username, password):
		"""Log the user.

		Args:
			username (str): The account username.
			password (str): The account password.

		Returns:
			IMAP4 or IMAP4_SSL: The object describing the connection.
		"""
		self.server.login(username, password)
		logger.info('Logged as {}.'.format(self.hostname))
		return self.server