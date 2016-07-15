from struct import pack
from bluepy.btle import Peripheral, UUID

on = pack('bb', 0x01, 0x00)
off = pack('bb', 0x00, 0x00)

def enable_notifications(device):
    device.writeCharacteristic(0x000f, on)

def disable_notifications(device):
    device.writeCharacteristic(0x000f, off)
