#from bluepy.btle import Peripheral, UUID
from error.error_handle import log_error
from sql.sqlite_ import insert_db
from data import read
from notifications import enable_notifications

def control(device):


    enable_notifications(device)

    try:

        while True:

            device.waitForNotifications(6000)
                            
            data = read(device)
            print data

            sql_data = [data]
            #insert_db(sql_data)

    except Exception as err:
            method = 'control()'
            log_error(method,err)
            print 'error at control():',err
