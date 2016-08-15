import struct
from time import sleep
from bluepy.btle import Peripheral, UUID
from datetime import datetime

#setup UUIDs for the name of device and data service
nameUUID = UUID('2A00')
serviceUUID = UUID('2221')


def read(device):
        #set current timestamp
        now = datetime.now() 
        time = datetime.now()

        #read device name    
        name = device.getCharacteristics(uuid=nameUUID)[0].read()

        #read data sent from node
        service = device.getCharacteristics(uuid=serviceUUID)[0]

        #unpack all data sent from node
        package = struct.unpack('iffb', service.read())
        brightness = package[0]
        temp = '{:.2f}'.format(package[1])
        SimbleeTemp = '{:.2f}'.format(package[2])
        RSSI = package[3]
        data = (device.deviceAddr, name, time, temp, SimbleeTemp, brightness, RSSI)

        return data
