#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

#stdlib
import os, sys
from subprocess import call
from datetime import datetime
from email.utils import parseaddr

#https://github.com/liris/websocket-client
## sudo pip install --user websocket-client
from websocket import create_connection

print("PID: {0}\nIf you can't quite, run 'kill {0}'\n".format(os.getpid()))

def main(ws):
	first = True
	while True:
		result =  ws.recv()
		email = result[1:].split(":")[0]
		if first and'@' in parseaddr(email)[1]:
			call(["echo '{0}' | pbcopy".format(email)], shell=True)
			print (email+" was copied to clipboard")
			first = False
		else:
			print("Recieved:{1} {0}\n".format(result, datetime.now()))
	ws.close()

if __name__ == '__main__':
	try:
		ws = create_connection("wss://dropmail.me/websocket")
		main(ws)
	except KeyboardInterrupt:
		sys.exit(0)
		ws.close()
