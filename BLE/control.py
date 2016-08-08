#!/bin/sh
import threading
from bluepy.btle import Peripheral, UUID
from error.error_handle import log_error
from sql.sqlite_ import insert_db
from data import read
from notifications import enable_notifications
from cleanup import cleanup
from time import sleep

def connect(address, exit, connecting):
    connection = False

    while not connection:    
        try:
            if connecting.empty():
                connecting.put(1)
                cleanup(address)
                device = Peripheral(address, 'random')

                print address, "connected"
                connection = True
                connecting.get()

        except KeyboardInterrupt:
            exit.put(1)
            quit()

        except Exception as err:
                method = 'connect()'
                log_error(method,err)
                print 'error at connect():',err
                connecting.get()
                sleep(3)
    sleep(2)
    enable_notifications(device)
    return device

def control(address, queue, connecting, exit):
    run = 10

    device = connect(address, exit, connecting)    

    t = threading.currentThread()

    while (run):

        try:
            device.waitForNotifications(6000)
            
            data = read(device)
            queue.put(data)

            sql_data = [data]
            #insert_db(sql_data)
            
        except KeyboardInterrupt:
                exit.put(1)
                run = False
                quit()

        except Exception as err:
                method = 'control()'
                log_error(method,(address +' '+ str(err)))
                print 'error at control():', address, ' ',err
                if str(err) == "Device disconnected":
                    device = connect(address, exit, connecting)
                else: 
                    run = False

            

