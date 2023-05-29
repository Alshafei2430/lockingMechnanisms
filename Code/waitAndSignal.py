import threading

lock = threading.Lock()
condition = threading.Condition(lock)

def critical_section():
    print(f"Entered critical section for thread {threading.get_ident()}")
    # do some critical work here
    print(f"Exiting critical section for thread {threading.get_ident()}")

def wait_and_signal(counter):
    with condition:
        condition.wait()
        critical_section()
        counter += 1
        print(f"Thread {threading.get_ident()} finished. Counter: {counter}")
        condition.notify()

# create three counters
counters = [0, 0, 0]

# create three threads
threads = []
for i in range(3):
    t = threading.Thread(target=wait_and_signal, args=(counters[i],))
    threads.append(t)

# start all threads
for t in threads:
    t.start()

# signal all threads to wake up
with condition:
    condition.notify_all()
