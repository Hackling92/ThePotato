import gps_read as gps
import IMU
from EKF import ExtendedKalmanFilter

import numpy as np
import time

#SEE NOTES ON WEBSITE
#nbviewer.jupyter.org/github/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/11-Extended-Kalman-Filters.ipynb
#home.wlu.edu/~levys/kalman_tutorial/kalman_13.html

cgps = gps.gps_read()
IMU.initIMU()

PTPEKF = ExtendedKalmanFilter(4,4,0)

#Not sure if i need to define my time step here, or if I can just use the dt from time.time between samples

class PTP:

	def __init__(self):

		print("...PTP INITIALIZING...")		
		#Set initial starting position via read gps and read accel/read mag/read gyro
		#Define F via taylor series expansion eye(x) + array() * dt
		self.zlat,self.zlon,self.zbrg,self.zvel = cgps.gpsread()
		PTPEKF.x = [self.zlat,self.zlon,self.zbrg,self.zvel]
                #accx = IMU.readACCx()
                #accy = IMU.readACCy()
                #accz = IMU.readACCz()

                #CACCx = accx / numpy.sqrt(accx * accx + accy * accy + accz * accz)
                #CACCy = accy / numpy.sqrt(accx * accx + accy * accy + accz * accz)

#               self.x0 = np.matrix([self.zlat,self.zlon,self.zbrg,self.zvel])
#               self.z0 = np.matrix([self.zlat,self.zlon,self.zbrg,self.zvel])
		print("...PTP READY...")
		print("Init x: ",PTPEKF.x)
		print("GPS at t0: ",self.zlat,self.zlon,self.zbrg,self.zvel)

	def raw_read(self):
		return self.zlat,self.zlon,self.zbrg,self.zvel

	def ptp_read(self):
		return PTPEKF.x[0],PTPEKF.x[1],PTPEKF.x[2],PTPEKF.x[3]

	def predict_update(self):
		#NEED TO INCLUDE A FUNCTION IN THE PTP PROGRAM TO SPECIFY A NEW R VALUE IF THE GPS DATA IS INVALID TO PREVENT IT BEING UESD
		#CANT LEAVE AN OPEN CRASH LIKE THAT IN FINAL PROGRAM
		self.zlat,self.zlon,self.zbrg,self.zvel = cgps.gpsread()
		self.z = [self.zlat,self.zlon,self.zbrg,self.zvel]
		PTPEKF.predict_update(self.z,HJ,Hx)
#		print("Predict_update complete - Updated values below")

def HJ(x):
	return np.eye(4)

def Hx(x):
	return x
