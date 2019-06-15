import threading
import time

class Token:
    def __init__(self):
        pass


class Bucket:
    def __init__(self, N):
        self.buckets = 0
        self.max = N
        self.lock = threading.Lock()
        self.cv1 = threading.Condition()
        t1 = threading.Thread(target=self.generate_token, args=())
        t1.start()

    def generate_token(self):
        while True:
            with self.cv1:
                while self.buckets == self.max:
                    print ("bucket is full, let's wait")
                    self.cv1.wait()
                print ("bucket has room for token ", self.buckets)
                #self.cv1.wait_for(lambda: self.buckets != self.max)
                time.sleep(0.5) # 100 ms
                self.lock.acquire()
                self.buckets += 1
                self.lock.release()

    def extract_token(self, packets):
        self.lock.acquire()
        self.buckets -= packets
        self.lock.release()
        with self.cv1:
            self.cv1.notify()

    def isValid(self, packet):
        return self.buckets - packet >= 0

bucket = Bucket(11)
packets = [idx for idx in range(1,100)]

while packets:
    time.sleep(1)
    packet = packets.pop(0)
    if bucket.isValid(packet):
        bucket.extract_token(packet)
        print ("passing packet ", packet, " bucket size ", bucket.buckets)
    else:
        print ("droping packet ", packet, " bucket size ", bucket.buckets)
