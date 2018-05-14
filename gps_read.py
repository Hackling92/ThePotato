import serial
import socket

class gps_read:

    def __init__(self):
        self.ser = serial.Serial('/dev/serial0', 9600, timeout=1)

    def gpsread(self):
        line = str(self.ser.readline())
#        print(line)
        cline = line.split(',')
#        print(cline)
        while "GPGGA" not in line:
            line = str(self.ser.readline())
            cline = line.split(',')

        if "GPGGA" in line:
            latitude = cline[2]
            lat_dir = cline[3]
            longitude = cline[4]
            lon_dir = cline[5]
            qual = cline[6]
            speed = 0.0
            bearing = 0.0
#            print(cline)
            return (latitude,lat_dir,longitude,lon_dir,qual,speed,bearing)
#			if "GPRMC" in line:
#				if (cline[2] == 'V'):
#					qual = 0
#				else:
#					qual = 1
#				latitude = cline[3]
#				lat_dir = cline[4]
#				longitude = cline[5]
#				lon_dir = cline[6]
#				speed = cline[7]
#				bearing = cline[8]
#				print cline
#				return(latitude,lat_dir,longitude,lon_dir,qual,speed,bearing)
#		print "Finished"
        return line

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

