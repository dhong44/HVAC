import time, datetime
def log_error(method,err): #trace the error and write it to a txt
    timestamp = datetime.datetime.now()
    record = str(timestamp) + ','  + method + ',' + str(err) +  '\n'
    infile = open('error/error.txt','a')
    infile.write(record)
    infile.close()
