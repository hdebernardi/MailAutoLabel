#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas, csv, os

def _getPath(username):
	"""Get the absolute path of username with .csv suffix.
	Parameters
	----------
	username : string
		The username of mailbox.

	Returns
	-------
	string
		The absolute path of 'data/{}.csv'.format(username)
	"""
	root = os.getcwd()
	rel_path = os.path.join('data', username + ".csv")
	return os.path.join(root, rel_path)


def getMailsFromCsv(username):
	"""Get mails from a csv file.
	Parameters
	----------
	username : string
		The username of mailbox.
	Returns
	-------
	list
		A one dimension array containing mails.
	"""
	mails = []
	filepath = _getPath(username)

	with open(filepath, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		[mails.append(row) for row in reader]

	return mails


def saveMailsToCsv(username, mails, verbose=False):
	"""Save mails to a csv file.
	Parameters
	----------
	username : string
		The username of mailbox.
	mails : list
		A list of emails.
	Returns
	-------
	bool
		True on success, False on fail.
	"""
	path = _getPath(username)
	if verbose:
		print('Saving mails from {} mailbox in {}'.format(username, path))

	df = pandas.DataFrame(mails)
	df.to_csv(_getPath(username))
	return True