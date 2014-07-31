import os, twiml
from client import StockzClient
from flask import Flask, request, abort

# Application #

app = Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.secret_key = os.urandom(16)

# Client #

client = StockzClient()

# Functions #

def get_response(message):
	if not isinstance(message, basestring):
		raise TypeError('message must be a string')

	return twiml.response(twiml.message(message))

# Routes #

@app.route('/sms', methods = ['POST'])
def twilio():
	if not 'From' in request.form or not 'Body' in request.form:
		abort(500)

	sender = request.form['From']
	body = request.form['Body']

	if len(body) == 0:
		abort(500)

	body_split = body.split()
	action = body_split[0]

	if len(body_split) > 1:
		data = (' ').join(action[1:])
	else:
		data = None

	response = client.send_request(action, sender, data)

	return get_response(response)

# Server #

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)
