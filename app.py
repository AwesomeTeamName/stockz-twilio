import yaml, os, twiml
from client import StockzClient
from flask import Flask, request

# Application #

app = Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.secret_key = os.urandom(16)

# Errors #

errors = yaml.load(open('errors.yml', 'r'))

# Client #

client = StockzClient()

# Functions #

def get_response(message):
	if not isinstance(message, basestring):
		raise TypeError('message must be a string')

	return twiml.response(twiml.message(message))

def get_message(name):
	if not isinstance(errors, dict):
		return 'Unknown error.'

	if not name in errors['errors']:
		return 'Unknown error.'

	return str(errors['errors'][name])

# Routes #

@app.route('/sms', methods = ['POST'])
def twilio():
	if not 'From' in request.form or not 'Body' in request.form:
		return get_message('internal_error')

	sender = request.form['From']
	body = request.form['Body']

	if len(body) == 0:
		return get_message('internal_error')

	body_split = body.split()
	action = body_split[0]

	if len(body_split) > 1:
		data = (' ').join(action[1:])
	else:
		data = None

	response = client.send_request()

	return get_response('Hello, user!')

# Server #

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)
