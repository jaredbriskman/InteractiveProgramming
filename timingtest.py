import time

next_loop = time.time()

while True:
    next_loop += 1
    print 'hi'
    time.sleep(next_loop - time.time())
