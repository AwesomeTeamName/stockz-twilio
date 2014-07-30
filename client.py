import socket

class StockzClient():
	
	def __init__(self, host = '127.0.0.1', port = 1337):
		if not isinstance(host, basestring):
			raise TypeError('host must be a string')

		if not isinstance(port, int):
			raise TypeError('port must be an int')

		self._address = (host, port)
			
	def execute(self, data, timeout = 5):
		if not isinstance(data, basestring):
			raise TypeError('data must be a string')

		if not isinstance(timeout, int):
			raise TypeError('timeout must be an int')

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(self._address)
		sock.settimeout(timeout)

		sock.sendall(data)

		response = sock.recv(2048)

		sock.close()

		if not isinstance(response, basestring):
			return None

		return response
