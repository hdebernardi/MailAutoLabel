#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib
import chardet
from email.parser import HeaderParser
import email
import re
import bs4

list_response_pattern = re.compile(
	r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

class IMAP_Parser:
	"""TODO
	"""
	def __init__(self):
		pass

	def _parse_flags(self, flags):
		"""Parse the given flags.

		Args:
			flags (bytes): The flags given as bytes.

		Returns:
			list: The flags parsed as a list of bytes.
		"""
		return [imaplib.ParseFlags(flag) for flag in flags if len(flags) != 0]

	def _parse_header(self, header, encoding='utf-8'):
		"""Parse the given header.

		Args:
			header ()
		Returns:
			Message :
		"""
		return HeaderParser().parsestr(header[0][1].decode(encoding))

	def _decode_content(self, message):
		content = message.get_payload(decode=True)
		charset = message.get_content_charset('utf-8')
		try:
			return content.decode(charset, 'ignore')
		except LookupError:
			return content.decode(charset.replace('-', ''), 'ignore')
		except AttributeError:
			return content

	def _parse_text(self, text, encoding='utf-8'):
		"""Parse the given text.

		Args:
			text (bytes):

		Returns:

		"""
		mail = email.message_from_bytes(text[0][1])
		for part in mail.walk():
			if part.get_content_type() == 'text/plain':
				return 'PLAIN'
				#return self._decode_content(mail)
			elif part.get_content_type() == 'text/html':
				return 'HTML'
				#return get_rid_of_html(self._decode_content(mail))

		return 'NOTHING'

		def _parse_folder(self, folder):
			"""Parse the given folder.
			"""
			list_response_pattern = re.compile(
				r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

			match = list_response_pattern.match(folder.decode('utf-8'))
			flags, delimiter, mailbox_name = match.groups()
			mailbox_name = mailbox_name.strip('"')
			return (flags, delimiter, mailbox_name)


		def get_rid_of_html(self, str_as_html):
			"""TODO
			"""
			soup = bs4.BeautifulSoup(str_as_html, 'html.parser')

			# remove script and style elements
			[script.extract() for script in soup(['script', 'style'])]

			text = soup.get_text()

			# Divise en lignes et enlève les espaces à gauche et à droite sur chacune d'elles
			lines = (line.strip() for line in text.splitlines())

			# break multi-headlines into a line each
			chunks = (phrase.strip() for line in lines for phrase in line.split(' '))

			# add space between lines
			text = ' '.join(chunk for chunk in chunks if chunk)

			return text