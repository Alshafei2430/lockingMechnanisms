import threading

class ReadersWritersLock:
    def __init__(self):
        self.mutex = threading.Lock()
        self.resource_lock = threading.Lock()
        self.resource_available = threading.Semaphore(0)
        self.read_count = 0

    def acquire_read(self):
        with self.mutex:
            self.read_count += 1
            if self.read_count == 1:
                self.resource_lock.acquire()
        print(f"Reader {threading.current_thread().name} is reading shared resource")
        self.mutex.release()

    def release_read(self):
        with self.mutex:
            self.read_count -= 1
            if self.read_count == 0:
                self.resource_lock.release()
        print(f"Reader {threading.current_thread().name} released the read lock")

    def acquire_write(self):
        self.resource_lock.acquire()
        print(f"Writer {threading.current_thread().name} is writing shared resource")

    def release_write(self):
        self.resource_lock.release()
        print(f"Writer {threading.current_thread().name} released the write lock")

shared_resource = "Initial Value"
read_write_lock = ReadersWritersLock()

# Function for readers to access shared resource
def read_shared_resource():
    for i in range(5):
        read_write_lock.acquire_read()
        # ... read shared resource ...
        read_write_lock.release_read()

# Function for writers to access shared resource
def write_shared_resource():
    for i in range(5):
        read_write_lock.acquire_write()
        # ... write shared resource ...
        read_write_lock.release_write()

# Example usage
threads = []
for i in range(3):
    threads.append(threading.Thread(target=read_shared_resource, name=f"Reader {i+1}"))
for i in range(2):
    threads.append(threading.Thread(target=write_shared_resource, name=f"Writer {i+1}"))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
