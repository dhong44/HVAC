import threading
from Queue import Queue
from bluepy.btle import Peripheral, UUID
from cleanup import cleanup
from control import control
from packet_interval import set_interval
from clothing_prediction import parse_temp, predict_clothing
from pmv_calculation import PMV

def dict_avg(dict):
    sum = 0
    for i in dict:
        sum += float(dict[i])
    avg = float(sum) / len(dict)
    return avg

if __name__ == '__main__':

    threads = []
    device= []
    queue = Queue()

    MAC = ['CC:9B:84:26:0F:AC',
           'C1:2E:06:21:9D:CF']

    temp = dict()
    humidity = dict()

    for address in MAC:
        cleanup(address)
        device.append(Peripheral(address, 'random'))
        print address, "connected"

    sixAmTemp = parse_temp()

    for i in device:
        t = threading.Thread(target=control, args=[i,queue],)
        threads.append(t)
        t.start()

    while True:
        data = queue.get()

        temp[data[0]] = data[3]
        temp_avg = dict_avg(temp)

        #extract humidity
        #calculate average humidity

        Icl = predict_clothing(sixAmTemp, temp_avg)
        pmv = PMV(Temperature = temp_avg, Icl = Icl)

        print "pmv: ", pmv
