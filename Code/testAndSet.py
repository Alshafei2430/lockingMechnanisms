import threading

tas_lock = threading.Lock()
locked = False

counter = 0

def critical_section():
    global counter
    # Simulate some work
    for i in range(5):
        counter += 1

def tas_acquire(thread_id):
    global locked
    while True:
        with tas_lock:
            if not locked:
                locked = True
                print(f"Thread {thread_id} acquired the lock")
                return
            else:
                print(f"Thread {thread_id} is waiting for the lock")

def tas_release(thread_id):
    global locked
    with tas_lock:
        locked = False
        print(f"Thread {thread_id} released the lock")

def worker(thread_id):
    tas_acquire(thread_id)
    print(f"Thread {thread_id} entered the critical section")
    critical_section()
    print(f"Thread {thread_id} exited the critical section")
    tas_release(thread_id)

# Start multiple threads to execute the worker function
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Counter value:", counter)