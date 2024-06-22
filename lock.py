import threading
lock = threading.Lock() # build lock object

def lock_acquire():
	lock.acquire() # use lock operate
	
def release_lock():
	lock.release()
	
