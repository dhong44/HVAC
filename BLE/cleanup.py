import subprocess
import os



def cleanup(address):

    output = subprocess.check_output("sudo hcitool con", shell=True)

    for i in range( 0, len(output)-17):
        
        if output[i:i+17] == address:
            os.system('bt-device -d %s' %address)
