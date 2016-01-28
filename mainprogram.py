"""
this code to do flowing tasks:
1. Parsing command from Zm->UART,
2. Update data if exist and data is properly
3. If data not exist then create new data in counter_history

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
executeLimit = "1"
dbName = 'db.sqlite3'

#dictionary of machine name and short address
machine_name_dict = {}


ser = serial.Serial(port='/dev/ttyUSB0',baudrate=19200,timeout=30.0)

def convertcmd2bytes(shortadd,energy,product):
    cmd = (shortadd).to_bytes(2,'big') + (energy).to_bytes(2,'big') + (product).to_bytes(2,'big')
    return cmd

def parsecommandfromzm():
    line = ser.readline()
    print(line)
    
    new = str(line).split("\'")[1]
    new = new.replace("\r\n","")
    parse           = new.split(" ")[1:]
    #print(len(parse),'\r\n')
    if len(parse) == 28: 
        # header parsing
        #im_len          = parse[0]
        #im_type         = parse[1] + parse[2]
        #im_group        = parse[3] + parse[4]
        #im_cluster      = parse[5] + parse[6]
        im_src_add       = parse[8] + parse[7]
        #im_src_endpoint = parse[9]
        #im_des_endpoint = parse[10]
        #im_was_brdcast  = parse[11]
        #im_lqi          = parse[12]
        #im_sec          = parse[13]
        #im_seq          = parse[18]
        #im_pay          = parse[19]
        # msg parsing
        im_msg_cmd      = chr(int('0x' + parse[20],16))
        nameLSB         = chr(int('0x' + parse[22],16))
        nameMSB         = chr(int('0x' + parse[21],16))
        im_msg_name     = nameMSB + nameLSB
        im_msg_energy   = int('0X' + parse[23] + parse[24],16)
        im_msg_product  = int('0X' + parse[25] + parse[26],16)
        print(im_src_add, im_msg_name, im_msg_cmd, im_msg_energy, im_msg_product)
        return (im_src_add, im_msg_name, im_msg_cmd, im_msg_energy, im_msg_product)
    else:
        return (None, None, None, None, None)

""" this function to shutdown meet deadline machine and update remain time
"""
def checkMaintaintime():
    # connect database
    con = db.connect(dbName)
    cur = con.cursor()
    # get short address from machine name
    global machine_name_dict
    try:
        sql = """
        SELECT machine_name, maintain_time 
        FROM django_social_app_maintain_schedule 
        JOIN django_social_app_machine
        ON django_social_app_maintain_schedule.machine_id = django_social_app_machine.id 
        """
        rows = cur.execute(sql)
        # fetchall return type is 'list'
        rows = rows.fetchall()

        
        for row in rows:
            maintain_time = datetime.strptime(row.maintain_time, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            time_remain = maintain_time - now
            time_remain_hours = time_remain.days * 24 + time_remain.seconds // 3600
           
            if time_remain_hours < 0:
                disableMachine.append(row[3])
                #send command to module to disable machine
                if row.machine_name in machine_name_dict:
                    machineAdd = machine_name_dict[row.machine_name]
                    print("shutdown comamnd \r\n")
                    ser.write(b'<X')
                    ser.write(bytearray(row.machine_name,'utf-8'))
                    ser.write((int('0x'+machineAdd,16)).to_bytes(2,'big'))
                    ser.write(b'XXXX')
                else:
                    print("Disable-Machine Address Missing")

    except:
        print("update fail")

    finally:
        con.close()
        print("close database")


"""
read command from UART
update according counter database 
command rx update-machine-xxx(counter)-xxx(energy)
command tx rstnewday-machine-xxx(counter)-xxx(energy)
command tx fix-machine-xx(counter)-xxx(energy)
"""
def updateCurrentCounter(machineName,machineAdd,machineCounter,machineEnergy):
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
            print("data exist, update it")
            if (machineCounter) >= x[0][1] and (machineEnergy) > x[0][2]:
                # proper data, add to update list
                sqlDataMany.append(((machineCounter),(machineEnergy),(x[0][3])))
                print("append and wait for update:")
                print(sqlDataMany)

            elif (machineCounter) < x[0][1] and (machineEnergy) < x[0][2]:
                # send command to zigbee module to fix error data of board
                print("send reset command for ZM!")
                ser.write(b'<R')
                ser.write(bytearray(machineName,'utf-8'))
                ser.write((int('0X'+machineAdd,16)).to_bytes(2,'big'))
                ser.write((x[0][2]).to_bytes(2,'big'))
                ser.write((x[0][1]).to_bytes(2,'big'))
                print("Error, data of counter is smaller in database!")
                """
                print("update command \r\n")
                ser.write(b'<')
                #time.sleep(0.004)
                ser.write(b'R')
                #time.sleep(0.004)
                ser.write(b'K')
                #time.sleep(0.004)
                ser.write(b'4')
                #time.sleep(0.004)
                ser.write((23208).to_bytes(2,'big'))
                #time.sleep(0.004)
                ser.write((3).to_bytes(2,'big'))
                #time.sleep(0.004)
                ser.write((108).to_bytes(2,'big'))"""
        elif len(x) == 0:
            # the first data of machine or insert normally
            sql = "SELECT id FROM django_social_app_machine WHERE machine_name=\'"+machineName+"\'"
            machineid = cur.execute(sql)
            machineid = machineid.fetchall()
            print("Update later, according to old data")
            if machineCounter > 10:
                # send clear command
                ser.write(b'<C')
                ser.write(bytearray(machineName,'utf-8'))
                ser.write((int('0X'+machineAdd,16)).to_bytes(2,'big'))
                ser.write(b'0000')
                #ser.write(b')
            else:
                """ Proper new data """
                if len(machineid):
                    machineid = machineid[0][0]
                    sql = """
                    INSERT INTO django_social_app_counter_history(machine_id,counter,energy,save_time)
                    VALUES (""" + str(machineid) + "," + str(machineCounter) +\
                     "," + str(machineEnergy) + "," +\
                    "DATETIME('now','localtime'))"
                    print(sql)
                    cur.execute(sql)
                    con.commit()
                    print("insert new data for: ",machineName)
                else:
                    print("machine not exist")

        else:
            print("error!, too many data in one day")
    finally:    
        for i in todaydata:
            print(i)
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
        print("Execute Many")
        if len(sqlDataMany) > 1:
            con = db.connect(dbName)
            cur = con.cursor()
            try:
                for data in sqlDataMany:
                    sql = " UPDATE django_social_app_counter_history " +\
                    "SET counter = " + str(data[0]) + ",energy=" + str(data[1])+\
                    " WHERE id=" + str(data[2])
                    print(sql)
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
    """
    print("read new line \r\n")
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
    """
    global machine_name_dict

    rxadd,rxname, rxcmd,rxenergy,rxproduct = parsecommandfromzm()
    if rxadd != None and rxname != None:
        # update machine short address in global dictionary
        machine_name_dict[rxname] = rxadd;
        # let execute command from zigbee module
        if(rxcmd == 'U'):
            print("Receive a update command from: ",rxadd,rxname)
            updateCurrentCounter(rxname, rxadd, rxproduct, rxenergy)
            # execute update many
            executeSqlMany() 
        else:
            """do nothing"""










def main():
    #schedule.every(10).minutes.do(checkMaintaintime)
    global checkMaintaintime_next
    checkMaintaintime_next = datetime.now()

    try:
        while 1:
            #print("Before: ", datetime.now()) 
            updateCounter()
            #print("After : ", datetime.now())
            

    finally:
        print("close serial port")
        ser.close()

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it
