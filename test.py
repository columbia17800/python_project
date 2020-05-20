
import threading
import asyncio
import time

def event_loop():
	for i in range(10):
		time.sleep(1)
		print("whatever")

event_loop()()


