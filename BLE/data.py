import struct
from time import sleep
from bluepy.btle import Peripheral, UUID
from datetime import datetime

nameUUID = UUID('2A00')
serviceUUID = UUID('2221')

def read(device):
        now = datetime.now() 
        time = datetime.now()
        time = str(now.month) +'.' + str(now.day) + '.' + str(now.year) + ' ' + str(now.hour) + ':%02d' %now.minute + ':%02d' %now.second
    
        name = device.getCharacteristics(uuid=nameUUID)[0].read()

        service = device.getCharacteristics(uuid=serviceUUID)[0]

        package = struct.unpack('iffb', service.read())

        brightness = package[0]
        temp = '{:.2f}'.format(package[1])
        SimbleeTemp = '{:.2f}'.format(package[2])
        RSSI = package[3]

        data = (device.deviceAddr, name, time, temp, SimbleeTemp, brightness, RSSI)


        return data
