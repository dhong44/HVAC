from struct import pack
from time import sleep
from bluepy.btle import Peripheral, UUID
from error.error_handle import log_error

def set_interval(device, seconds):

    #try:
        
    char = device.getCharacteristics(uuid='2222')[0]

    delay = pack('i', int(seconds))
    
    char.write(delay)

    #except Exception as err:
    #    method = 'set_interval()'
    #    log_error(method,err)
    #    print 'error at set_interval():',err

        
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage:\n %s <mac-address> [time]" % sys.argv[0])
    address = sys.argv[1]
    seconds = sys.argv[2]
    
    device = Peripheral(address, 'random')
    set_interval(device, seconds)
    
