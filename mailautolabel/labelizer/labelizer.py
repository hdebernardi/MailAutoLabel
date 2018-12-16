#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas
import numpy

class MAILLabelizer:
	"""Class in charge of mail labelization.
	"""
	def __init__(self, username, messages):
		self.username = username
		self.messages = messages

	def _split_messages(self):
		X_labelized = []
		X_unlabelized = []

		for message in self.messages:
			if message['folder'] and message['folder'].lower() != 'inbox':
				X_labelized.append(message)
			else:
				X_unlabelized.append(message)

		return {'labelized' : X_labelized, 'unlabelized': X_unlabelized}

	def predict(self):
		"""
		"""
		data = self._split_messages()

		if len(data['labelized']) == 0 or len(data['unlabelized']) == 0:
			return []

		X = pandas.DataFrame(data['labelized']).drop(['folder'], axis=1)
		y = numpy.ravel(pandas.DataFrame(data['labelized'])['folder'])
		X_tar = pandas.DataFrame(data['unlabelized']).drop(['folder'], axis=1)

		"""# TF-IDF vectorizer"""
		vectorizer = TfidfVectorizer(analyzer="word")
		X_vec = vectorizer.fit_transform(X['body']) #.values.astype('U'))
		X_vec = pandas.DataFrame(
			X_vec.todense(), columns=vectorizer.get_feature_names())

		X_tar_vec = vectorizer.transform(X_tar['body']) #.values.astype('U'))
		X_tar_vec = pandas.DataFrame(
			X_tar_vec.todense(), columns=vectorizer.get_feature_names())

		"""# Logistic regression"""

		classifier = LogisticRegression(class_weight='balanced')
		classifier.fit(X_vec, y)
		predicts = classifier.predict(X_tar_vec)
		return numpy.column_stack((X_tar, predicts))