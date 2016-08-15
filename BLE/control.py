#!/bin/sh
import threading
from bluepy.btle import Peripheral, UUID
from error.error_handle import log_error
from sql.sqlite_ import insert_db
from data import read
from notifications import enable_notifications
from cleanup import cleanup
from time import sleep

#connect to device
def connect(address, exit, connecting):
    #set variable to track connection
    connection = False

    #retry connection until it is successful
    while not connection:    
        try:
            # connect only if another attempt is not in progress
            if connecting.empty():
                #log a current connection is in progress
                connecting.put(1)
                #disconnect previous connections and connect to peripheral
                cleanup(address)
                device = Peripheral(address, 'random')

                #print and log successful connection and remove current connection attempt
                print address, "connected"
                connection = True
                connecting.get()

        #if keyboard interrupt is pressed exit program
        except KeyboardInterrupt:
            exit.put(1)
            quit()

        #log errors 
        except Exception as err:
                method = 'connect()'
                log_error(method,err)
                print 'error at connect():',err
                #remove connection attempt and wait to allow other peripherals to connect
                connecting.get()
                sleep(3)
    
    #after connection enable notifications from peripheral
    sleep(2)
    enable_notifications(device)
    return device

def control(address, data_queue, connecting, exit):
    run = True

    #connect to device
    device = connect(address, exit, connecting)    

    #infinitely loop to read from raspberry pi
    while (run):

        try:
            #wait for notifications from node then read data and send to queue 
            device.waitForNotifications(6000)
            data = read(device)
            data_queue.put(data)

            #insert data into local sql database
            sql_data = [data]
            insert_db(sql_data)

        #if keyboard interrupt is pressed exit program            
        except KeyboardInterrupt:
                exit.put(1)
                run = False
                quit()

        #log errors
        except Exception as err:
                method = 'control()'
                log_error(method,(address +' '+ str(err)))
                print 'error at control():', address, ' ',err
                #if disconnection occurs reconnect to peripheral
                if str(err) == "Device disconnected":
                    device = connect(address, exit, connecting)
                else: 
                    run = False

            

