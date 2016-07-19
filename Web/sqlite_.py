import sqlite3

def insert(settings):
    conn = sqlite3.connect('control.db')
    cur = conn.cursor()
    cur.executemany("INSERT INTO temperature (Heat, Cool, ts) VALUES (?, ?, datetime('now', 'localtime'));", settings)
    conn.commit()
    conn.close()


        
    
def create_table():
    conn = sqlite3.connect('control.db')
    conn.execute(
                '''CREATE TABLE temperature
                   (Heat BOOLEAN,
                   Cool BOOLEAN,
                   ts DATETIME
                   );'''
                  )
    conn.close()
    
