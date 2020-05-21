#!usr/bin/env python3
import sys
import os.path as path
sys.path.append( path.dirname(path.dirname(path.abspath(__file__))) )

from src.mainserver import MainServer

server = MainServer()
server.serve_forever()
server.shutdown()
