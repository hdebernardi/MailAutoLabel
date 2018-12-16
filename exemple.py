#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from mailautolabel.imap.imap import IMAPMain
from mailautolabel.labelizer.labelizer import MAILLabelizer

################################################################################
# logger configuration
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setLevel(logging.INFO)
FORMATTER = logging.Formatter('%(asctime)s - %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
################################################################################

hostname=''
username=''
password=''

imap = IMAPMain(hostname=hostname, username=username, password=password)

################################################################################
# list folders
folders = imap.get_folders()
[print(folder) for folder in folders]
################################################################################


################################################################################
# get all messages with all keys
messages = imap.get_messages()
[print(message) for message in messages]
################################################################################


################################################################################
# get all messages with only a few header keys
messages = imap.get_messages(
	header_keys=['from', 'subject', 'date', 'from', 'to'])
################################################################################


################################################################################
# get all messages from 'Inbox' folder
messages = imap.get_messages(
	folder=['Inbox']
)
################################################################################


################################################################################
# get all messages from <your_friend@domain.com> with unseen flag
messages = imap.get_messages(
	search={
		'unseen': True,
		'from': 'your_friend@domain.com'
	}
)
################################################################################

# NOTE THAT ALL THE ABOVE ARGUMENTS CAN BE COMBINED

################################################################################
# save the messages into a csv file
import pandas, os
path_to_save = os.path.abspath('data/{}.csv'.format(username))
pandas.DataFrame(messages).to_csv(path_to_save)
################################################################################


################################################################################
# get the labelizer class and predict folders
labelizer = MAILLabelizer(username=username, messages=messages)

predictions = labelizer.predict()
for predict in predictions:
	print('{} >> {}'.format(predict[0], predict[-1]))
################################################################################


################################################################################
# move a message into his predicted folder with a flag to know that it
# has been mooved by the library
print(messages[0])
imap.mark_message_with_flag(messages[0]['uid'], 'AutoLabel')
# the following line add the 'Unseen' flag to messages predicted because
# download it with RFC822 removes it
imap.mark_message_with_flag(messages[0]['uid'], 'Unseen')
imap.move_message(messages[0]['uid'], destination_folder='@dest_folder')
################################################################################
