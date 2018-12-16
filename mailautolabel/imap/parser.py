#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module consists of utils functions.
Its primary goal is to return human readable formats.
"""

import re
import imaplib
import bs4
import flanker.mime

RAW_FOLDER_PATTERN = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

def parse_folder(folder: bytes) -> str:
	"""Parse the given folder.
	"""
	match = RAW_FOLDER_PATTERN.match(folder.decode('utf-8'))
	_flags, _delimiter, mailbox_name = match.groups()
	mailbox_name = mailbox_name.strip('"')
	return mailbox_name

def get_rid_of_html(html_text: str) -> str:
	"""Remove the html script and style elements from a string.
	"""
	soup = bs4.BeautifulSoup(html_text, 'lxml')

	# remove script and style elements
	for script in soup(['script', 'style']):
		script.extract()

	text = soup.get_text()
	return text

def parse_flags(flags: bytes) -> list:
	"""Parse the given flags.

	Args:
		flags: The flags given as bytes.

	Returns:
		The flags parsed as a list of bytes.
	"""
	return [imaplib.ParseFlags(flag) for flag in flags]

def parse_mail(raw_mail: bytes):
	"""Parse the given mail.

	Args:
		mail (bytes):

	Returns:

	"""
	return flanker.mime.from_string(raw_mail)
