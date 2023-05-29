import threading

def Semaphore(value=1):
    mutex = threading.Lock()
    sem = threading.Condition(mutex)
    count = value

    def acquire():
        nonlocal count
        with sem:
            while count == 0:
                print(f"{threading.current_thread().name} is waiting for semaphore")
                sem.wait()
            count -= 1
            print(f"{threading.current_thread().name} acquired semaphore")

    def release():
        nonlocal count
        with sem:
            count += 1
            print(f"{threading.current_thread().name} released semaphore")
            sem.notify()

    return acquire, release

# Example usage
acquire, release = Semaphore()

def worker():
    acquire()
    print(f"{threading.current_thread().name} in critical section")
    # Do some work
    release()
    print(f"{threading.current_thread().name} released critical section")

threads = []
for i in range(5):
    thread = threading.Thread(target=worker, name=f"Worker {i}")
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()