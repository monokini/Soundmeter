
# import required module
import os
import sqlite3
import datetime
import time

grafana = False
drive = 'D'
clearDb = True

directory = drive+":/programming/soundmeter/raw"

if grafana==True:
    conn = sqlite3.connect(drive+':/programming/soundmeter/soundmeter_grafana.s3db')
else:
    conn = sqlite3.connect(drive+':/programming/soundmeter/soundmeter.s3db')

c = conn.cursor()
if clearDb==True:
    conn.execute('DELETE FROM data')
    conn.commit()

 
# iterate over files in that directory
for filename in os.scandir(directory):
    db55 = 0
    db60 = 0
    db65 = 0
    db70 = 0
    
    cnt = 0
    if filename.is_file():
        f = open(filename.path, "r")
        for x in f:
            list = x.split(",", 4)
            if len(list)>1:
                cnt = cnt + 1
                date_array = list[0].split("-", 3)
                time_array = list[1].split(":", 3)
                if float(list[2]) > 70.0:
                    db70 = db70 + 1
                
                if float(list[2]) > 65.0:
                    db65 = db65 + 1
                    
                if float(list[2]) > 60.0:
                    db60 = db60 + 1
                                    
                if float(list[2]) > 55.0:
                    db55 = db55 + 1
                    
                value = (int(round(float(list[2]),0))) # rounded dezibel value
                    
                date_time = datetime.datetime(int(date_array[2]),int(date_array[1]),int(date_array[0]),int(time_array[0]),int(time_array[1]),int(time_array[2]))
               
                if grafana==True:               
                    unix_time = (time.mktime(date_time.timetuple()))
                    data = (unix_time, value)
                    conn.execute("INSERT INTO data (time,value) VALUES (?,?)", data)
                else:
                    data = (int(date_array[2]),int(date_array[1]),int(date_array[0]),int(time_array[2]),int(time_array[1]),int(time_array[0]),value)
                    conn.execute("INSERT INTO data (y,m,d,h,n,s,db) VALUES (?,?,?,?,?,?,?)", data)
  
        f.close()
        conn.commit()
        print("=====================================================")
        print(filename.path)
        print("70dB:", db70, "/", round((db70*100)/cnt,1), '%')
        print("65dB:", db65, "/", round((db65*100)/cnt,1), '%')
        print("60dB:", db60, "/", round((db60*100)/cnt,1), '%')
        print("55dB:", db55, "/", round((db55*100)/cnt,1), '%')
        
c.close()
conn.close()


