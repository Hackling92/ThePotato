import gps_read as gps
import IMU
import time

cgps = gps.gps_read()
IMU.initIMU() 

def main():

	while True:
                cgps = gps.gps_read()
		lat,lon,h,vel = cgps.gpsread()
#		print(gps_str)
#		accel_x = IMU.readACCx()
#		accel_y = IMU.readACCy()
#		accel_z = IMU.readACCz()
#		print("Accel: X: %d Y: %d Z: %d"%(accel_x,accel_y,accel_z))

		print("Latitude: %f"%(lat))
		print("Longitude: %f"%(lon))
		print("Bearing: %f"%h)
		print("Velocity: %f"%vel)

		time.sleep(1)
		

main()
