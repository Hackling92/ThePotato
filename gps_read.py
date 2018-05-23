import serial
import socket

class gps_read:

	def __init__(self):
		self.ser = serial.Serial('/dev/serial0', 9600, timeout=1)

	def gpsread(self):
		line = self.ser.readline()
#		cline = line.split(',')
		while "GPRMC".encode('utf-8') not in line:
#                       print("Looping:")
			line = self.ser.readline()
#                       print(line)
#	               	cline = line.split(',')
#
#		if "GPGGA" in line:
#			latitude = cline[2]
#			lat_dir = cline[3]
#			longitude = cline[4]
#			lon_dir = cline[5]
#			qual = cline[6]
#			speed = 0.0
#			bearing = 0.0
#			print(cline)
#			return(latitude,lat_dir,longitude,lon_dir,qual,speed,bearing)
#		if "GPRMC" in line:
#			if (cline[2] == 'V'):
#				qual = 0
#			else:
#				qual = 1
#			latitude = cline[3]
#			lat_dir = cline[4]
#			longitude = cline[5]
#			lon_dir = cline[6]
#			speed = cline[7]
#			bearing = cline[8]
#			print cline
#			return(latitude,lat_dir,longitude,lon_dir,qual,speed,bearing)
#		print "Finished"
#		print("Done looping")
		gdata = str(line).split(',')
		if gdata[2] == 'A':
			if gdata[4] == 'N':
				lat = float(gdata[3]) / 100.0
			else:
				lat= -1 * float(gdata[3]) / 100.0
			if gdata[6] == 'E':
				lon = float(gdata[5]) / 100.0
			else:
				lon = -1 * float(gdata[5]) / 100.0
			brg = float(gdata[8])
			vel = float(gdata[7])			

#	      		print("Latitude: %f"%(lat))
#               	print("Longitude: %f"%(lon))
#			print("Bearing: %f"%brg)
#			print("Velocity: %f"%vel)
		else:
#                      	print("Invalid GPS Data")
			lat = 0.0
			lon = 0.0
			brg = 0.0
			vel = 0.0

		return lat,lon,brg,vel

#def main():
#	lat = ''
#	lon = ''
#	lat_d = ''
#	lon_d = ''
#	qual = ''
#	speed = ''
#	bearing = ''
#	lat,lat_d,lon,lon_d,qual,speed,bearing = readgps()
#	print("Latitude:  %s %s"%(lat,lat_d))
#	print("Longitude: %s %s"%(lon,lon_d))
#	print("Speed: %s :: Bearing: %s"%(speed,bearing))
#	print("Valid: %s"%qual)
#	lat,lat_d,lon,lon_d,qual,speed,bearing = readgps()
#	print("Latitude:  %s %s"%(lat,lat_d))
#	print("Longitude: %s %s"%(lon,lon_d))
#	print("Speed: %s :: Bearing: %s"%(speed,bearing))
#	print("Valid: %s"%qual)
#
#main()
