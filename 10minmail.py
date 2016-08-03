#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

#https://github.com/liris/websocket-client
## sudo pip install --user websocket-client
from websocket import create_connection

class mailbox(object):
	"""10 minute mailbox"""
	def __init__(self):
		super(mailbox, self).__init__()
		self.ws = create_connection("wss://dropmail.me/websocket")
		self.next = self.ws.recv
		self.close = self.ws.close
		self.email = self.next()[1:].split(":")[0]
		self.next()

def main(box):
	#stdlib
	import sys
	from json import loads
	from subprocess import call
	from datetime import datetime
	
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

if __name__ == '__main__':
	import os
	print("PID: {0}\nIf you can't quite, run 'kill {0}'\n".format(os.getpid()))
	try:
		box = mailbox()
		main(box)
	except KeyboardInterrupt:
		box.close()
		sys.exit(0)
