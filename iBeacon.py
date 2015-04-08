#!/usr/bin/python3

##--Michael duPont
##--iBeacon.py : iBeacon Interface Using BlueZ
##--Provides a Python class to control a BlueZ-based iBeacon via terminal commands
##--2015-04-08

#Installation
#sudo apt-get install libbluetooth-dev bluez

import os , time

#I use a Blink(1) as a status light. GPIO LEDs or anything similar will work as well
useBlink1 = True

class iBeacon:
	#Init takes company ID, major, minor, and power
	#Company ID is the hex string while the rest can be the hex string or int value
	def __init__(self , companyID , areaID , unitID , power):
		self.__companyID = companyID
		if type(areaID) == int: self.__areaID = self.intToFormattedHex(areaID , 2)
		else: self.__areaID = areaID
		if type(unitID) == int: self.__unitID = self.intToFormattedHex(unitID , 2)
		else: self.__unitID = unitID
		if type(power) == int: self.__power = self.intToFormattedHex(power , 1)
		else: self.__power = power
	
	#Starts the iBeacon transmitting. Bluez works asyncronously
	def startBeacon(self):
		os.system('sudo hciconfig hci0 up')
		os.system('sudo hciconfig hci0 leadv')
		os.system('sudo hciconfig hci0 noscan')
		os.system('sudo hcitool -i hci0 cmd 0x08 0x0008 {0} {1} {2} {3} 00'.format(self.__companyID , self.__areaID , self.__unitID , self.__power))
		if useBlink1: os.system('blink1-tool --green')
		print('iBeacon up')
	
	#For the duration of "seconds", replace old broadcast packet with one whose
	#minor value is incremented by one. After duration, broadcast reverts to
	#original packet.
	def triggerEvent(self , seconds):
		self.triggerStart()
		time.sleep(seconds)
		self.triggerEnd()
	
	#Replace old broadcast packet with one whose minor value is incremented by one
	def triggerStart(self):
		triggerInt = int('0x'+self.__unitID[:2]+self.__unitID[3:],0) + 1
		#print(triggerInt)
		triggerString = self.intToFormattedHex(triggerInt , 2)
		#print(triggerString)
		os.system('sudo hcitool -i hci0 cmd 0x08 0x0008 {0} {1} {2} {3} 00'.format(self.__companyID , self.__areaID , triggerString , self.__power))
		if useBlink1: os.system('blink1-tool --red')
	
	#Broadcast reverts to original packet
	def triggerEnd(self):
		os.system('sudo hcitool -i hci0 cmd 0x08 0x0008 {0} {1} {2} {3} 00'.format(self.__companyID , self.__areaID , self.__unitID , self.__power))
		if useBlink1: os.system('blink1-tool --green')
	
	#Stop transmission of iBeacon
	def endBeacon(self):
		os.system('sudo hciconfig hci0 noleadv')
		if useBlink1: os.system('blink1-tool --off')
		print('iBeacon down')
	
	# int 60 , 2 -> string '00 3C' // int 60 , 1 -> string '3C'
	def intToFormattedHex(self , intIn , pairs):
		hexTemp = '{0:x}'.format(abs(intIn)).zfill(pairs*2).upper()
		hexOut = hexTemp[:2]
		for i in range(pairs-1): hexOut += ' ' + hexTemp[2*i+2:2*i+4]
		return hexOut


if __name__ == '__main__':
	#Company ID, Area ID, Unit ID, and Power Setting
	cid = '1E 02 01 1A 1A FF 4C 00 02 15 E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 61'
	aid = 0  # -> '00 00'
	uid = 0  # -> '00 00'
	power = -202  # -> 'CA'
	#Initialize iBeacon
	ib = iBeacon(cid , aid , uid , power)
	#Start broadcasting
	ib.startBeacon()
	time.sleep(5)
	#Enter triggered state for 5 seconds
	ib.triggerEvent(5)
	time.sleep(5)
	#End broadcasting
	ib.endBeacon()
