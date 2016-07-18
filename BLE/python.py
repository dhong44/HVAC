import threading
from Queue import Queue
from bluepy.btle import Peripheral, UUID
from cleanup import cleanup
from control import control
from packet_interval import set_interval
from clothing_prediction import parse_temp, predict_clothing

def worker(num):
    """thread worker function"""
    print 'Worker:', num
    return

if __name__ == '__main__':

    sixAmTemp = parse_temperature()

    threads = []
    device= []
    queue = Queue()

    MAC = ['CC:9B:84:26:0F:AC',
           'C1:2E:06:21:9D:CF']

    for address in MAC:
        cleanup(address)
        device.append(Peripheral(address, 'random'))
        print address, "connected"

    for i in device:
        t = threading.Thread(target=control, args=[i,queue],)
        threads.append(t)
        t.start()

    while True:
        print(queue.get())
