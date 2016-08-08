from btle import Peripheral, UUID

simblee = Peripheral('CC:9B:84:26:0F:AC', 'random')

serviceUUID = UUID('2A00')

char = simblee.getCharacteristics(uuid = serviceUUID)[0]

char.write('Simblee')

print char.read()

simblee.disconnect()
