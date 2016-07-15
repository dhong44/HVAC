import threading
from bluepy.btle import Peripheral, UUID
from cleanup import cleanup
from control import control
from packet_interval import set_interval

def worker(num):
    """thread worker function"""
    print 'Worker:', num
    return

if __name__ == '__main__':
    threads = []
    device= []

    MAC = ['CC:9B:84:26:0F:AC',
           'C1:2E:06:21:9D:CF']

    for address in MAC:
        cleanup(address)
        device.append(Peripheral(address, 'random'))
        print address, "connected"

    for i in device:
        t = threading.Thread(target=control, args=(i,))
        threads.append(t)
        t.start()


    
