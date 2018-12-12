#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################
#from .string_helper import detect_encoding, get_rid_of_html
#import mailparser
import chardet
from email.parser import HeaderParser
import email
import re
import bs4
list_response_pattern = re.compile(
	r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
############################################################

from .connection import IMAP_Connection
from .message import IMAP_Message
from .parser import IMAP_Parser
from .query import IMAP_Query

import logging
import sys
import imaplib
import itertools

logger = logging.getLogger()

class IMAP_Main():
	"""The main class in charge of interaction with a remote mailbox.

	If you are new with IMAP using Python, I strongly recommand you to read :
	https://pymotw.com/3/imaplib/

	For further reading, you should read the RFC :
	https://tools.ietf.org/html/rfc3501

	Args:
		hostname (str): The server's address.
		username (str): The account username.
		password (str): The account password.
		port (int): The server's port. IMAP uses 143 by default, 993 with SSL.
		ssl (bool): Should we use SSL encryption ? Default is True.
	"""
	def __init__(self, hostname, username, password, port=None, ssl=True):
		self.hostname = hostname
		self.username = username
		self.password = password
		#self.access_token = None

		self.header_keys = None

		self.server = IMAP_Connection(hostname=hostname, port=port, ssl=ssl)
		self.connection = self.server.login(self.username, self.password)

		self.parser = IMAP_Parser()
		self.query = None

	def __enter__(self):
		"""Used for context manager.

		See : https://www.python.org/dev/peps/pep-0343/
		"""
		return self

	def __exit__(self, type, value, traceback):
		"""Used for context manager.

		See : https://www.python.org/dev/peps/pep-0343/
		"""
		return self.logout()

	def logout(self):
		"""Used for context manager.

		See : https://www.python.org/dev/peps/pep-0343/
		"""
		self.connection.close()
		self.connection.logout()
		logger.info('Logged out.')

	def copy_message(self, uid, destination_folder):
		"""Copy a message into a folder.

		Args:
			uid (int): The unique id of the message. Be carreful, the uid is only unique into a folder.
			destination_folder (str) : The destination folder.

		Returns:
			TODO
		"""
		logger.info('Copy UID {} to {}.'.format(
			uid, destination_folder))
		return self.connection.copy(uid, destination_folder)

	def move_message(self, uid, destination_folder):
		"""Move a message into a destination folder.

		Since not every IMAP server implements the move function, we will use a combination of copy/delete to do the job.

		Args:
			uid (int): The unique id of the message. Be carreful, the uid is only unique into a folder.
			destination_folder (str) : The destination folder.

		Returns:
			TODO
		"""
		logger.info('Move UID {} to {} folder.'.format(uid, destination_folder))
		if self.copy_message(uid, destination_folder):
			self.delete_message(uid)

	def mark_flag(self, uid, flag):
		"""Mark a message with a given flag.
		"""
		logger.info("Mark UID {} with \\{} FLAG".format(uid, flag))
		self.connection.uid('STORE', uid, '+FLAGS', '(\\{})'.format(flag))

	def delete_message(self, uid):
		"""Delete a message.
		TODO
		"""
		self.connection.expunge()

	def get_messages(self, **kwargs):
		"""Get messages.
		"""

		#message_instance = IMAP_Message

		# we try to get a folders key from kwargs, if we don't find it,
		# it means the user didn't specify a folder, so we look into all folders
		folders = kwargs.get('folders', None)
		if not folders:
			folders = self._get_parsed_folders()
		self.header_keys = kwargs.get('header_keys', None)

		del kwargs['header_keys']
		del kwargs['folders']
		# construct the query
		self.query = IMAP_Query(kwargs=kwargs)

		messages = []

		for folder in folders:
			messages.append(self._get_messages_from_folder(folder))

		return list(itertools.chain.from_iterable(messages))
		#return [self._get_messages_from_folder(folder) for folder in folders]

	def get_folders(self):
		"""List all folders of current selected mailbox.

		Returns:
			tuple[str, list[bytes]]: The first string is the status response, you should always check it to prevent errors ('OK'). The list contains the folder names as they're appears on the imap server.
		"""
		logger.info('Getting folders.')
		return self.connection.list()


	############################################################
	def _get_uids(self, folder):
		"""Get all the messages' identifiants from a folder.

		Args:
			folder (str): The folder's name where we should search for uids.

		Returns:
			list: A list of messages' uids if some, an empty list otherwise.
		"""
		search_str = self.query.build()
		status, uids = self.connection.search(None, '({})'.format(search_str))

		#print(search_str)

		if status != 'OK':
			logger.warning('Status reponse isn\'t OK')
			return []

		#logger.info('Found {} uids into {}.'.format(0, folder))
		return uids[0].split() if uids[0] is not None else []

	def _get_parsed_folders(self):
		"""Parse the folders' strings to extract name.
		"""
		status, raw_folders = self.get_folders()
		return [self.parser._parse_folder(folder)[2] for folder in raw_folders]

	def _fetch_email_by_uid(self, uid, folder):
		logger.info('Fetch message with UID {}'.format(uid))

		if self.header_keys:
			request = '(BODY.PEEK[HEADER.FIELDS ({})] BODY.PEEK[TEXT])'.format(' '.join(self.header_keys))
		else:
			request = '(BODY.PEEK[HEADER] BODY.PEEK[TEXT])'

		status, raw_mail = self.connection.fetch(uid, request)
		#logger.debug('Header contains : {}'.format(header))
		status, raw_flags = self.connection.fetch(uid, '(FLAGS)')
		#logger.debug('Flags contains : {}'.format(flags))

		header = self.parser._parse_header(raw_mail)
		text = self.parser._parse_text(raw_mail)
		flags = self.parser._parse_flags(raw_flags)

		email_dict = {}
		for key, value in header.items():
			email_dict[key] = value

		email_dict['folder'] = folder
		email_dict['uid'] = uid
		email_dict['body'] = text
		email_dict['flags'] = flags

		return email_dict

	def _get_messages_from_folder(self, folder):
		logger.info('Getting messages from {}'.format(folder))
		self.connection.select(folder)

		messages = []
		for uid in self._get_uids(folder):
			messages.append(self._fetch_email_by_uid(uid, folder))
		return messages
		#return [self._fetch_email_by_uid(uid) for uid in self._get_uids(folder)]