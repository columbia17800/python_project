import time
import asyncio
import functools
from threading import Thread, current_thread, Event
from concurrent.futures import Future

class B(Thread):
    def __init__(self, start_event):
        Thread.__init__(self)
        self.loop = None
        self.tid = None
        self.event = start_event

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.tid = current_thread()
        self.loop.call_soon(self.event.set)
        self.loop.run_forever()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)

    def add_task(self, coro):
        """this method should return a task object, that I
          can cancel, not a handle"""
        def _async_add(func, fut):
            try:
                ret = func()
                fut.set_result(ret)
            except Exception as e:
                fut.set_exception(e)

        f = functools.partial(self.loop.create_task, coro)
        if current_thread() == self.tid:
            return f() # We can call directly if we're not going between threads.
        else:
            # We're in a non-event loop thread so we use a Future
            # to get the task from the event loop thread once
            # it's ready.
            fut = Future()
            self.loop.call_soon_threadsafe(_async_add, f, fut)
            return fut.result()

    def cancel_task(self, task):
        self.loop.call_soon_threadsafe(task.cancel)

    def interrupt(self):
        self.loop.call_soon_threadsafe(functools.partial(print, "Hello"))


async def test():
    while True:
        print("running")
        await asyncio.sleep(1)

event = Event()
b = B(event)
b.start()
event.wait() # Let the loop's thread signal us, rather than sleeping
time.sleep(5)
t = b.add_task(test()) # This is a real task
time.sleep(5)
b.interrupt()
time.sleep(5)
b.stop()