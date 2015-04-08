#!/usr/bin/python3

##--Michael duPont
##--gatewayScanner.py : Access-granting iBeacon scanner
##--Query Azure SQL db to determine one-time access for device emitting an iBeacon
##--2015-04-08

import blescan , pyodbc , sys , os
from time import sleep

useBlink1 = True

#Connection Information
dsn = 'sqlserverdatasource' #From odbc.ini
user = 'user@server'
password = 'password'
database = 'mydatabase'
con_string = 'DSN={0};UID={1};PWD={2};DATABASE={3};'.format(dsn,user,password,database)

conn = pyodbc.connect(con_string)
cursor = conn.cursor()

#Convert 64:80:65:f9:2e:96,e20a39f473f54bc4a12f17d1ad07a961,0000,0003,c5
#Into  E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 61 00 00 00 03 C5 00  
def sanitizeBLEPacket(blePacket):
	blePacket = blePacket[blePacket.find(',')+1:].upper()
	blePacket = blePacket.replace(',' , '')
	blePacket = ' '.join(a+b for a,b in zip(blePacket[::2], blePacket[1::2]))
	return blePacket + ' 00'

#Queries beaconDB for rows where 'text' == blePacket
#Returns first ID from query results else empty string
def queryAzureDB(blePacket):
	cursor.execute("select id, text from [Item] where text = ?" , blePacket) #Edit query info
	rows = cursor.fetchall()
	#print(rows)
	if rows: return rows[0][0]
	return ''

#Delete row from table where 'id' == key
def deleteRowWithPacket(key):
	deletedCount = cursor.execute("delete from [Item] where id='" + key + "'").rowcount #Edit delete info
	conn.commit()
	print('Deleted: ' + str(deletedCount))

#Handling function for each ble packet foud by parse_events
def respondToFoundPacket(blePacket):
	blePacket = sanitizeBLEPacket(blePacket)
	key = queryAzureDB(blePacket)
	if key:
		print('Azure query returned True for: ' + blePacket)
		print('With this key: ' + key)
		if useBlink1: os.system('blink1-tool --green')
		deleteRowWithPacket(key)
	else:
		print('Packet not found: ' + blePacket)
		if useBlink1: os.system('blink1-tool --red')
	sleep(10)
	if useBlink1: os.system('blink1-tool --off')
	return None

def main():
	#Open and configure ble scanning
	devId = 0
	try:
		sock = blescan.getBLESocket(devId)
		print("Now looking for iBeacon packets")
	except:
		print("Error accessing bluetooth device")
		sys.exit(1)
	blescan.hci_le_set_scan_parameters(sock)
	
	#Begin Scanning
	blescan.hci_enable_le_scan(sock)
	
	#Main Loop
	while True:
		returnedList = blescan.parse_events(sock, 10) #This line will only return when at least one packet is found
		print("----------")
		for beacon in returnedList:
			#print(beacon)
			respondToFoundPacket(beacon)

if __name__ == '__main__':
	main()
