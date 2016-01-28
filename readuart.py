import serial
import os
import time

ser = serial.Serial(port="/dev/tty.usbserial-A600ICLA",baudrate=19200)
x = open('log.txt','a')
im_src_add = ""

def convertcmd2bytes(shortadd,energy,product):
	"""
	Message format CMD MACHINE-NAME SHORT-ADD ENERGY COUNTER
	"""
	#cmd = bytearray(cmdtype,'utf-8') + bytearray(machinename,'utf-8') + 
	cmd = (shortadd).to_bytes(2,'big') + (energy).to_bytes(2,'big') + (product).to_bytes(2,'big')

	return cmd
"""
try:
	while ser.isOpen():"""

try:
	while ser.isOpen():
		
		kcmd = input('Enter W for Write, R to Readline\r\n')
		if kcmd == 'R':
			line = ser.readline()
			print(line)
			
			new = str(line).split("\'")[1]
			new = new.replace("\r\n","")
			parse 			= new.split(" ")[1:]
			if len(parse) > 24: 
				# header parsing
				im_len 			= parse[0]
				im_type 		= parse[1] + parse[2]
				im_group 		= parse[3] + parse[4]
				im_cluster 		= parse[5] + parse[6]
				im_src_add 		= '0x' + parse[8] + parse[7]
				im_src_endpoint = parse[9]
				im_des_endpoint = parse[10]
				im_was_brdcast 	= parse[11]
				im_lqi 			= parse[12]
				im_sec		 	= parse[13]
				im_seq 			= parse[18]
				im_pay 			= parse[19]
				# msg parsing
				im_msg_cmd      = parse[20]
				im_msg_name     = parse[21] + parse[22]
				im_msg_energy   = '0x' + parse[23] + parse[24]
				im_msg_product  = '0x' + parse[25] + parse[26]
				
		elif kcmd == 'W':
			"""
			zmcmd = input('Command = ')
			print('\r\n')
			zmshortname = input('Module Short Add = ')
			print('\r\n')
			zmmacname = input('Module Name = ')
			print('\r\n')
			zmenergy = input('Module Energy = ')
			print('\r\n')
			zmproduct = input('Module Product = ')
			print('\r\n')
			#ser.write(bytearray(zmcmd+zmmacname,'utf-8'))"""
			ser.write(b'<')
			#time.sleep(0.004)
			ser.write(b'R')
			#time.sleep(0.004)
			ser.write(b'K')
			#time.sleep(0.004)
			ser.write(b'4')
			#time.sleep(0.004)
			ser.write((int(im_src_add,16)).to_bytes(2,'big'))
			#time.sleep(0.004)
			ser.write((3).to_bytes(2,'big'))
			#time.sleep(0.004)
			ser.write((108).to_bytes(2,'big'))
			#data = convertcmd2bytes(7626,1000,1000)
			#ser.write(data)
		else:
			print('doing nothing')
		"""	finally:
				ser.close()
				x.close()"""
finally:
	ser.close()
