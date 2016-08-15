import subprocess
import os



def cleanup(address):

    #save list of connections to string
    output = subprocess.check_output("sudo hcitool con", shell=True)

    #search connections for adress
    for i in range( 0, len(output)-17):
        #if address is found disconnect the address from device
        if output[i:i+17] == address:
            os.system('bt-device -d %s' %address)