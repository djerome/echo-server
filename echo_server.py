#!local/bin/python
#
# File: echo_server.py
#
#	Echoes message back to echo_client
#

import socket
import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler

# Initiatizations
receive_chunk = 16

# logging constants
log_file = "/var/log/conn_test/conn_test.log"
log_format = "%(asctime)s: %(message)s"
date_format = "%m/%d/%Y %X"

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create timed rotating file handler and set level to debug
fh = TimedRotatingFileHandler(log_file, when='D', interval=30, backupCount=12)
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

# add formatter to file handler
fh.setFormatter(formatter)

# add file handler to logger
logger.addHandler(fh)

# log program restart
logger.info('RESTART: ' + os.path.basename(__file__))

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 10000)
logger.info('Starting up on {} port {}'.format(*server_address))
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)

# Loop infinitely and wait for a connection
while True:
	connection, client_address = sock.accept()
	client_ip = client_address[0]
	client_fqdn = socket.gethostbyaddr(client_ip)
	print 'IP = ' + client_ip + ', FQDN = ' + client_fqdn[0]
	try:
		print('Connection from ' + str(client_address))

		# Receive the data in small chunks and
		# retransmit it
		while True:
			data = connection.recv(receive_chunk)
			print('received {!r}'.format(data))
			if data:
				print('Sending data back to ' + str(client_address))
				connection.sendall(data)
			else:
				logger.warn('No data from {0} ({1})'.format(client_fqdn, client_ip))
				print('No data from ' + str(client_address))
				break
	finally:
		# Clean # up # the # connection
		connection.close()
		print('Closing connection from ' + str(client_address))
