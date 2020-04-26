from threading import Timer


def raiseE():
	raise Exception

try:
	t = Timer(3.0, raiseE)
except Exception:
	print("at creation")
try:
	t.start()
except Exception:
	print("at starting")
print("inside function")