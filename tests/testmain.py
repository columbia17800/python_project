#!usr/bin/env python3
import sys
import os.path as path
sys.path.append( path.dirname(path.dirname(path.abspath(__file__))) )

from src.mainserver import MainServer
import threading

server = MainServer()
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
server_thread.join()
server.shutdown()
