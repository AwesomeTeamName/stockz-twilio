from flask import Response

TWIML_HEADER = '<?xml version="1.0" encoding="UTF-8" ?>'
TWIML_BODY = '<Response>\n\t{0}\n</Response>'
TWIML_FORMAT = '{header}\n{body}'

def generate(text):
	if not isinstance(text, basestring):
		raise TypeError('text must be a string')

	body = TWIML_BODY.format(text)
	response = TWIML_FORMAT.format(header = TWIML_HEADER, body = body)

	return response

def message(text):
	body = ('<Message>{0}</Message>').format(text)
	return generate(body)

def response(text):
	return Response(text, mimetype = 'text/xml')
