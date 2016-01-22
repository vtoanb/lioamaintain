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
#import schedule
import time

sqlDataMany = []
sqlManyTime = datetime.now() + timedelta(minutes=10)
checkMaintaintime_next = datetime.now()
#execute limit for sqlMany record
executeLimit = "10"
dbName = 'db.sqlite3'

""" this function to shutdown meet deadline machine and update remain time
    get all rows @ django_social_app_maintain_schedule
    if calculated remaintime different maintain_time in table then update it
    if calculated maintain time smaller than zero then disable machine

"""

#config serial

ser = serial.Serial(port='/dev/ttyUSB0',baudrate=115200,timeout=30.0)


def checkMaintaintime():
    # connect database
    con = db.connect(dbName)
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
        #disableMachine = []
        for row in rows:
            maintain_time = row[4].split(".")[0]
            maintain_time = datetime.strptime(maintain_time, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            time_remain = maintain_time - now

            time_remain_hours = time_remain.days * 24 + time_remain.seconds // 3600
            print "cal new remain: ",time_remain_hours,"--> in db: ", row[2]
            print "now: ",now,"with maintain_time: ",maintain_time
            if time_remain_hours != row[2]:
                #insert to sql command to update in database

                newItem = (time_remain_hours,row[0])
                sqlMany.append(newItem)
            #if time_remain_hours < 0:
            #    disableMachine.append(row[3])
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


"""
read command from UART
update according counter database 
command rx update-machine-xxx(counter)-xxx(energy)
command tx rstnewday-machine-xxx(counter)-xxx(energy)
command tx fix-machine-xx(counter)-xxx(energy)
"""
def updateCurrentCounter(machineName,machineCounter,machineEnergy):
    con = db.connect(dbName)
    cur = con.cursor()
    global sqlDataMany
    try:

        # get today table with machine name, counter,history and id-of-history-record
        sql = """
        SELECT machine_name, counter, energy, django_social_app_counter_history.id
        FROM django_social_app_counter_history
        JOIN django_social_app_machine
        ON django_social_app_counter_history.machine_id = django_social_app_machine.id
        WHERE DATE(save_time) = DATE('now','localtime')
        AND machine_name = \'""" + machineName + "\'"
        todaydata = cur.execute(sql)
        x = todaydata.fetchall()
        if len(x) == 1:
            print "data exist, update it"
            if machineCounter >= x[0][1] and machineEnergy > x[0][2]:
                # proper data, add to update list
                sqlDataMany.append((machineCounter,machineEnergy,(x[0][3])))
                print "append and wait for update:"
                print sqlDataMany

            elif machineCounter < x[0][1] or machineEnergy < x[0][2]:
                # send command to zigbee module to fix error data of board
                v = 'fix-' + unicode(x[0][0]) + '-' + unicode(x[0][1]) + '-' + unicode(x[0][2])
                ser.write(v)
                ser.write('\n')
                print "Error, data of counter is smaller in database!"
                print v
        elif len(x) == 0:
            """ 
                - insert new data in new day
                - check if data is larger then most close day then re-calcute it
                - send command to zigbee 
            """
            sql ="""SELECT counter, energy 
            FROM django_social_app_counter_history
            JOIN django_social_app_machine
            ON django_social_app_counter_history.machine_id = django_social_app_machine.id
            WHERE machine_name = \'""" + machineName + "\'" +\
            "ORDER BY save_time DESC LIMIT 1"
            lastdat = cur.execute(sql)
            lastdat = lastdat.fetchone()
            if len(lastdat) > 0:
                lastdat = lastdat[0]
                print "last data of" + machineName + " : " + lastdat
                print "new data" + machineCounter + " : " + machineEnergy
                # compare with latest data in database
                # if larger then reset in zigbee module
                if machineCounter >= lastdat[0] and machineEnergy >= lastdat[1]:
                    machineCounter = machineCounter - lastdat[0]
                    machineEnergy = machineEnergy = lastdat[1]
                    #update new data to zigbee
                    resetcmd = "rstnewday-" + machineName +"-" +\
                     unicode(machineCounter) + "-" + unicode(machineEnergy)
                    ser.write(resetcmd)
                    ser.write(b'\n')
                elif (machineCounter < lastdat[0] and machineEnergy > lastdat[1]) or\
                     (machineCounter > lastdat[0] and machineEnergy < lastdat[1]):
                    #in valid data
                    machineCounter = 0
                    machineEnergy = 0
            
            # the first data of machine or insert normally
            sql = "SELECT id FROM django_social_app_machine WHERE machine_name=\'"+machineName+"\'"
            machineid = cur.execute(sql)
            machineid = machineid.fetchall()
            if len(machineid):
                machineid = machineid[0][0]
                sql = """
                INSERT INTO django_social_app_counter_history(machine_id,counter,energy,save_time)
                VALUES (""" + unicode(machineid) + "," + unicode(machineCounter) +\
                 "," + unicode(machineEnergy) + "," +\
                "DATETIME('now','localtime'))"
                print sql
                cur.execute(sql)
                con.commit()
                print "insert new data for: " + machineName
            else:
                print "machine not exist"

        else:
            print "error!, too many data in one day"
    finally:    
        for i in todaydata:
            print i
        con.close()
"""
Update many data to django_social_app_counter_history
sqlDataMany : counter, energy, row_id
"""
def executeSqlMany():
    global sqlDataMany
    global sqlManyTime
    #execute if time is over or record limit is break
    #print len(sqlDataMany)
    if len(sqlDataMany) > int(executeLimit) or sqlManyTime < datetime.now():
        if len(sqlDataMany) > 1:
            con = db.connect(dbName)
            cur = con.cursor()
            try:
                for data in sqlDataMany:
                    sql = " UPDATE django_social_app_counter_history " +\
                    "SET counter = " + unicode(data[0]) + ",energy=" + unicode(data[1])+\
                    " WHERE id=" + unicode(data[2])
                    print sql
                    cur.execute(sql)
                con.commit()
                # reset sqlDataMany
                sqlDataMany = []
                sqlManyTime = datetime.now() + timedelta(minutes=10)
            finally:
                con.close()
        else:
            #if len still zero then
            sqlManyTime = datetime.now() + timedelta(minutes=10)
            


def updateCounter():
    print "read new line \r\n"
    line = ser.readline().replace('\n','')
    if 'update' in line:
        line = line.split('-')
        if len(line) == 4:
            machine = line[1]
            counter = int(line[2])
            energy  = int(line[3])
            #checkMaintaintime()
            #print "update counter history database"
            updateCurrentCounter(machine,counter,energy)
            print "try to execute waiting list to database"
            executeSqlMany()





def main():
    #schedule.every(10).minutes.do(checkMaintaintime)
    global checkMaintaintime_next
    checkMaintaintime_next = datetime.now()

    try:
        while 1:
            print "Before: ", datetime.now()
            updateCounter()
            print "After : ", datetime.now()
            

    finally:
        print "close serial port"
        ser.close()

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it
