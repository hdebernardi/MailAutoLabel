import logging
import chardet
import bs4

logger = logging.getLogger()

def detect_encoding(value):
	return chardet.detect(value)['encoding']

def my_encode(str_to_decode='', errors='strict'):
	"""TODO
	"""
	encoding = detect_encoding(str_to_decode)
	"""
	logger.debug('Encoding {} as {}. Errors are {}'.format(
		str_to_decode, encoding, errors))
	"""
	return str(str_to_decode, encoding, errors)

def my_decode(str_to_encode='', errors='strict'):
	"""TODO
	"""
	if isinstance(str_to_encode, str):
		return bytes(str_to_encode, errors).decode('utf-8')
	elif isinstance(str_to_encode, bytes):
		encoding = detect_encoding(str_to_encode)
		return str_to_encode.decode(encoding, errors=errors)

def get_rid_of_html(str_as_html):
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