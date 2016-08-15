import threading
from Queue import Queue
from control import control
from clothing_prediction import parse_temp, predict_clothing
from pmv_calculation import PMV

#calculate average of a dictionary
def dict_avg(dict):
    sum = 0
    for i in dict:
        sum += float(dict[i])
    avg = float(sum) / len(dict)
    return avg

if __name__ == '__main__':
    #setup threads
    threads = []
    
    #setup MAC addresses
    MAC = ['CC:9B:84:26:0F:AC',
           'C1:2E:06:21:9D:CF']

    #set temperature and humidity records
    temp = dict()
    humidity = dict()

    #setup queues 
    data_queue = Queue()
    exit = Queue()
    connecting = Queue()

    #start threads for each MAC address
    for address in MAC:
        t = threading.Thread(target=control, args=[address, data_queue, connecting, exit],)
        threads.append(t)
        t.start()
        
    #parse 6:00 AM temperature    
	sixAmTemp = parse_temp()

    while True:
        #read data if it's available'
        if not (queue.empty()):
            data = queue.get_nowait()

            #find average temperature
            temp[data[0]] = data[3]
            temp_avg = dict_avg(temp)
            
            #calculate the apparent temperature scale
            Icl = predict_clothing(sixAmTemp, temp_avg)
            pmv = PMV(Temperature = temp_avg, Icl = Icl)

            #something about humidity

            print "pmv, ", pmv        

        #exit if both threads have exited
        if exit.qsize() >= len(MAC):
            break
        

