#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

#stdlib
import os, sys
from json import loads
from subprocess import call
from datetime import datetime
from email.utils import parseaddr

#https://github.com/liris/websocket-client
## sudo pip install --user websocket-client
from websocket import create_connection

class mailbox(object):
	"""docstring for mailbox"""
	def __init__(self):
		super(mailbox, self).__init__()
		self.ws = create_connection("wss://dropmail.me/websocket")
		self.email = self.ws.recv()[1:].split(":")[0]
		self.ws.recv()

	def next(self):
		"""Returns the next message. Blocking."""
		return self.ws.recv()		

def main(box):
	call(["echo '{0}' | pbcopy".format(box.email)], shell=True)
	print (box.email+" was copied to clipboard")
	while True:
		result =  box.next()
		try:
			print("Recieved following at {0}".format( datetime.now()))
			for k in loads(result[1:]).items():
				print("\t%s: %s" % k)
		except:
			print("Recieved:{1} {0}\n".format(result, datetime.now()))

	ws.close()

if __name__ == '__main__':
	print("PID: {0}\nIf you can't quite, run 'kill {0}'\n".format(os.getpid()))
	try:
		box = mailbox()
		main(box)
	except KeyboardInterrupt:
		ws.close()
		sys.exit(0)
