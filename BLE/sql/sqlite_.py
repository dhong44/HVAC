import sqlite3
import datetime
def insert_db(data):
    conn = sqlite3.connect('sql/im_temp.db')
    cur = conn.cursor()
    cur.executemany("INSERT INTO Temp (mac, name, ts, temp_r, temp_f, brightness, RSSI) VALUES (?, ?, ?, ?, ?, ?, ?);", data)
    conn.commit()
    conn.close()

def create_table():
    conn = sqlite3.connect('im_temp.db')
    conn.execute(
                '''CREATE TABLE Temp
                   (mac         TEXT     NOT NULL,
                   name           TEXT    NOT NULL,
                   ts             Datetime    NOT NULL,
                   temp_r         Real,
                   ts2             Real,
                   temp_f           real,
                   Pressure         real,
                   Hummidty         real,
                   RSSI             real,
                   brightness       real,
                   switch           real
                   );'''
                  )
    conn.close()
# data=[row.replace('\n','').split(',') for row in file('temp.txt','r').readlines()]
# print data
# insert_db(data)
# cur = conn.cursor()
# # # cur.executemany("INSERT INTO Temp (mac, name, ts, temp_r, ts2, temp_f, Pressure, Hummidty) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", data)
# # # conn.commit()
# # # strftime('%Y-%m-%d %H:%M:%S', ...)
# # # s_d = cur.execute("SELECT * From temp where strftime('%H:%M:%S', ts) between '10:06:00' and '10:30:59'")
# # # s_d = cur.execute("SELECT * From temp where name = 'E1'")
# s_d = cur.execute("SELECT * From temp where temp_r between 19 and 21 order by temp_r")
# # s_d = cur.execute("SELECT max(temp_r) From temp where temp_r between 19 and 21")
# for rows in s_d:
#     print rows
# conn.close()


# if __name__ == '__main__':
    # data=[row.replace('\n','').split(',') for row in file('temp.txt','r').readlines()]
    # print data
    # d = [('aaaa', 'E2', datetime.datetime.now(), 21.65, 9, 7.22, 981.0, 84)]
    # # print len(d)
    # # insert_db(d)
    # conn = sqlite3.connect('im_temp.db')
    # cur = conn.cursor()
    # cur.execute("DELETE FROM temp where mac = 'aaaa'")
    # conn.commit()
    # # s_d = cur.execute("SELECT * FROM temp WHERE mac = 'aaaa'")
    # # for rows in s_d:
    # #     print rows
    # conn.close()

# conn = sqlite3.connect('im_temp.db')
# cur = conn.cursor()
# # # cur.execute("DELETE FROM temp WHERE mac = 'aaaa'")
# # # cur.commit()
# s_d = cur.execute("SELECT count(*) FROM temp where name='E3' and strftime('%Y-%m-%d %H:%M:%S', ts) between '2016-05-10 09:00:00' and '2016-05-10 10:00:00' ")
# for rows in s_d:
#     print rows
# conn.close()
    # create_table()
