"""
this code to do flowing tasks:
1. Update maintain_remaintime of all machines in database
2. Read counter from zigbee and update in database
3. Send command to zigbee to disable machine if it's maintain_remaintime < 0

"""

import time
import serial
import io
import sqlite3 as db
from datetime import datetime,timedelta


""" this function to shutdown meet deadline machine and update remain time
    get all rows @ django_social_app_maintain_schedule
    if calculated remaintime different maintain_time in table then update it
    if calculated maintain time smaller than zero then disable machine

"""

#config serial

ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600)


def checkMaintaintime():
    # connect database
    con = db.connect('db1.test')
    cur = con.cursor()
    
    try:
        rows = cur.execute("select * from django_social_app_maintain_schedule")
        # fetchall return type is 'list'
        rows = rows.fetchall()

        """ iterate all row and update maintain time if need
        0 : id
        1 : type
        2 : remain
        3 : machine_id
        4 : maintain_time
        """
        sqlMany =  []
        disableMachine = []
        for row in rows:
            maintain_time = row[4].split(".")[0]
            maintain_time = datetime.strptime(maintain_time, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            time_remain = maintain_time - now

            time_remain_hours = time_remain.days * 24 + time_remain.seconds // 3600
            if time_remain_hours != row[2]:
                #insert to sql command to update in database
                newItem = (time_remain_hours,row[0])
                sqlMany.append(newItem)
            if time_remain_hours < 0:
                disableMachine.append(row[3])
        #in the end execute all update element
        if len(sqlMany) > 0:
            try:
                print "try to update to database"
                cur.executemany("update django_social_app_maintain_schedule set maintain_time_remain=? where id=?",sqlMany)
                con.commit()
                print "update success!"

            except:
                print('update remain fail')
        else:
            print " nothing to update to database"

        #get the list of disable machien and then send to zigbee
        sql = """SELECT machine_name
        FROM django_social_app_machine
        JOIN django_social_app_maintain_schedule 
        ON django_social_app_machine.id = django_social_app_maintain_schedule.machine_id
        WHERE maintain_time_remain < 0
        """
        x = cur.execute(sql)
        command = x.fetchall()
        dismac = []


        for c in command:
            if c[0] not in dismac:
                dismac.append(c[0])
                v = unicode('shutdown-' + c[0] )
                ser.write(v)
                ser.write(b'\n')
        ser.write(b'\n')
        

        print dismac

    except:
        print "update fail"

    finally:
        con.close()
        print "close database"






def main():
    print "execute updatemaintaintime"
    checkMaintaintime()
    ser.close()

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it
