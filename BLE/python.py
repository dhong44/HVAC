import threading
from Queue import Queue
from control import control
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
    device = []

    MAC = ['CC:9B:84:26:0F:AC',
           'C1:2E:06:21:9D:CF']

    temp = dict()
    humidity = dict()

    queue = Queue()
    exit = Queue()
    connecting = Queue()

    for address in MAC:
        t = threading.Thread(target=control, args=[address,queue, connecting, exit],)
        threads.append(t)
        #t.read_data = True
        t.start()
        
	sixAmTemp = parse_temp()

    while True:
        if not (queue.empty()):
            data = queue.get_nowait()

            temp[data[0]] = data[3]
            temp_avg = dict_avg(temp)
            
            Icl = predict_clothing(sixAmTemp, temp_avg)
            pmv = PMV(Temperature = temp_avg, Icl = Icl)

            #something about humidity

            print "pmv, ", pmv        

        if exit.qsize() >= len(MAC):
            break
        

