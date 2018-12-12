#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from mailautolabel.imap import IMAP_Main
from mailautolabel.labelizer import MAIL_Labelizer

################################################################################
# logger configuration
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
	'%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
################################################################################
"""
hostname='imap-mail.outlook.com'
username='hippode@hotmail.fr'
password='Gains!bourg28'
"""
hostname='mail.gandi.net'
username='contact@hippolyte-debernardi.com'
password='B_94*lti!f'

imap = IMAP_Main(
	hostname=hostname,
	username=username,
	password=password)

# list folders
#status, folders = imap.get_folders()
#[print(folder) for folder in folders]

# get messages
messages = imap.get_messages(
	header_keys = ['from', 'subject', 'date', 'from', 'to'],
	#folders = ['Inbox'], # 'Univ', 'Meditation'],
	search = 'unseen'
)

#print(messages[0].keys())
#[print(message['uid']) for message in messages]
import pandas, os
path_to_save = os.path.abspath('data/{}.csv'.format(username))
pandas.DataFrame(messages).to_csv(path_to_save)

"""
# get the labelizer class and predict folders
labelizer = MAIL_Labelizer(
	username=username,
	messages=messages)

predictions = labelizer.predict()
for predict in predictions:
	print('{} >> {}'.format(predict[0], predict[-1]))
"""
#print(messages[3])
#print(imap.move_message(messages[3]['uid'], destination_folder='Abonnements'))