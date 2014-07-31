import yaml, os, twiml
from flask import Flask, request
from client import StockzClient

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

@app.route('/sms', methods = ['GET', 'POST'])
def twilio():
	return get_response('Hello, user!')

# Server #

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True)
