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