#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main module.
"""

import logging
import itertools

from mailautolabel.imap.connection import IMAPConnection
from mailautolabel.imap.message import get_normalized_message
from mailautolabel.imap.parser import parse_flags, parse_folder, parse_mail
from mailautolabel.imap.query import build_query

LOGGER = logging.getLogger()


class IMAPMain:
	"""The main class in charge of interaction with a remote mailbox.

	If you are new with IMAP using Python, I strongly recommand you to read :
	https://pymotw.com/3/imaplib/

	For further reading, you should read the RFC :
	https://tools.ietf.org/html/rfc3501

	Args:
		hostname: The server's address.
		username: The account username.
		password: The account password.
		port: The server's port. IMAP uses 143 by default, 993 with SSL.
		ssl: Should we use SSL encryption ? Default is True.
	"""
	def __init__(self, hostname: str, username: str, password: str, port: int = None, ssl: bool = True):
		self.hostname = hostname
		self.username = username
		self.password = password

		self.server = IMAPConnection(hostname=hostname, port=port, ssl=ssl)
		self.connection = self.server.login(self.username, self.password)

	def __enter__(self):
		"""Used for context manager.

		See : https://www.python.org/dev/peps/pep-0343/
		"""
		return self

	def __exit__(self, type_, value, traceback):
		"""Used for context manager.
		"""
		return self.logout()

	def logout(self):
		"""Used for context manager.
		"""
		self.connection.close()
		self.connection.logout()
		LOGGER.info('Logged out.')

	def get_folders(self):
		"""List all folders of current selected mailbox.

		Returns:
			tuple(str, list(bytes)
			The first string is the status response.
			The list contains the folder names as they're appears on the imap server.
		"""
		LOGGER.info('Getting folders.')
		_status, raw_folders = self.connection.list()
		return [parse_folder(folder) for folder in raw_folders]

	def copy_message(self, uid: int, destination_folder: str):
		"""Copy a message into a folder.

		Be carreful, the uid is only unique for @mailbox-@folder-@uid primary key.

		Args:
			uid: The message's identifiant.
			destination_folder: The destination folder.

		Returns:
			TODO
		"""
		LOGGER.info('Copy UID %s to %s.', uid, destination_folder)
		return self.connection.copy(uid, destination_folder)

	def move_message(self, uid: int, destination_folder: str):
		"""Move a message into a destination folder.

		Since not every IMAP server implements the move function,
		we will use a combination of copy/delete to do the job.

		Args:
			uid (int): The unique id of the message.
			Be carreful, the uid is only unique into a folder.
			destination_folder (str) : The destination folder.

		Returns:
			TODO
		"""
		LOGGER.info('Move UID %s to %s folder.', uid, destination_folder)
		if self.copy_message(uid, destination_folder):
			return self.delete_message(uid)
		return False

	def mark_message_with_flag(self, uid, flag):
		"""Mark a message with a given flag.
		"""
		LOGGER.info('Mark UID %s with \\%s FLAG', uid, flag)
		self.connection.store(uid, '+FLAGS', '(\\{})'.format(flag))

	def delete_message(self, uid):
		"""Delete a message.
		TODO
		"""
		print(uid)
		self.mark_message_with_flag(uid, 'Deleted')
		return self.connection.expunge()

	def get_messages(self, **kwargs):
		"""Get messages.
		"""
		# we try to get a folders key from kwargs, if we don't find it,
		# it means the user didn't specify a folder, so we look into all folders
		folders = kwargs.get('folders', None)
		if not folders:
			folders = self.get_folders()
		else:
			del kwargs['folders']

		header_keys = kwargs.get('header_keys', None)
		if header_keys is not None:
			del kwargs['header_keys']

		# construct the query
		query = build_query(kwargs=kwargs)

		messages = []
		for folder in folders:
			messages.append(self._get_messages_from_folder(folder, query, header_keys))
		return list(itertools.chain.from_iterable(messages))

################################################################################
################################################################################
################################################################################
	def _get_uids(self, folder, query):
		"""Get all the messages' identifiants from a folder.

		Args:
			folder (str): The folder's name where we should search for uids.

		Returns:
			list: A list of messages' uids if some, an empty list otherwise.
		"""
		self.connection.select(folder)
		_status, uids = self.connection.search(None, '({})'.format(query))

		#LOGGER.info('Found {} ids into {}.'.format(len(uids[0].split), folder))
		return uids[0].split() if uids[0] is not None else []

	def _fetch_email_by_uid(self, uid: int, folder: str, header_keys: list):
		"""
		"""
		#if self.header_keys:
		#	request = '(BODY.PEEK[HEADER.FIELDS ({})] BODY.PEEK[TEXT])'.format(
		#	' '.join(self.header_keys))
		#else:
		#	request = '(BODY.PEEK[HEADER] BODY.PEEK[TEXT])'
		#request = '(RFC822)'

		LOGGER.info('Fetching message with UID %s', uid)

		_status, raw_mail = self.connection.fetch(uid, '(RFC822)')
		_status, raw_flags = self.connection.fetch(uid, '(FLAGS)')

		mail = parse_mail(raw_mail[0][1])
		flags = parse_flags(raw_flags)

		return get_normalized_message(mail=mail, folder=folder, flags=flags, header_keys=header_keys)

	def _get_messages_from_folder(self, folder, query, header_keys):
		LOGGER.info('Getting messages from %s', folder)

		messages = []
		for uid in self._get_uids(folder, query):
			messages.append(self._fetch_email_by_uid(uid, folder, header_keys))
		return messages
