import yaml, os, twiml
from flask import Flask, request
from client import StockzClient

# Configuration #

try:
	config = yaml.load(open('config.yml', 'r'))

	if not isinstance(config, dict):
		raise Exception()
except:
	raise Exception('Invalid config.yml')

if 'flask' not in config or not isinstance(config['flask'], dict):
	raise Exception('Missing flask from config')

if 'client' not in config or not isinstance(config['client'], dict):
	raise Exception('Missing client from config')

# Application #

app = Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.secret_key = os.urandom(16)

# Client #

client = StockzClient(**config['client'])

# Routes #

@app.route('/sms', methods = ['GET', 'POST'])
def twilio():
	if 'From' not in request.form or 'Body' not in request.form:
		return twiml.response(twiml.message('Invalid action. Reply \'help\' for a list of actions.'))

	sender = request.form['From']
	body = request.form['Body']

	response = client.execute(body)

	if response is None:
		return twiml.response(twiml.message('Invalid action. Reply \'help\' for a list of actions.'))

	return twiml.response(twiml.message(response))

# Server #

if __name__ == '__main__':
	app.run(**config['flask'])
