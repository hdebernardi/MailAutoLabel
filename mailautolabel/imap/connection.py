#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module implements a simple IMAP connection.
"""

import logging
from imaplib import IMAP4, IMAP4_SSL

LOGGER = logging.getLogger()

class IMAPConnection:
	"""A class aimed to implement a simple IMAP connection.

	Args:
		hostname (str): The server's address.
		port (int): The server's port. IMAP uses 143 by default, 993 with SSL.
		ssl (bool): Should we use SSL encryption ? Default is True.
	"""
	def __init__(self, hostname: str, port: int = None, ssl: bool = True):
		self.hostname = hostname

		if ssl:
			self.port = port or 993
			self.server = IMAP4_SSL(host=self.hostname, port=self.port)
		else:
			self.port = port or 143
			self.server = IMAP4(host=self.hostname, port=self.port)

		LOGGER.info('Connection initialized for %s:%s %s',
		self.hostname, self.port, 'over SSL.' if ssl else '.')

	def login(self, username: str, password: str) -> IMAP4 or IMAP4_SSL:
		"""Log the user.

		Args:
			username: The account username.
			password: The account password.

		Returns:
			The object describing the connection.
		"""
		self.server.login(username, password)
		LOGGER.info("Logged as %s.", username)
		return self.server
