#!usr/bin/env python3
import sys
import os.path as path
sys.path.append( path.dirname(path.dirname(path.abspath(__file__))) )

from src.mainserver import MainServer
import threading
import time


server = MainServer()
server_thread = threading.Thread(target = server.serve_forever)
server_thread.start()
try:
	while True:
		time.sleep(0.5)
except KeyboardInterrupt:
	server.shutdown()
