import smbus as smb
import time
import math
import datetime
from LSM9DS1 import *

bus = smb.SMBus(1)

ACC_ADDRESS = LSM9DS1_ACC_ADDRESS

def writeACC(register,value):
	bus.write_byte_data(ACC_ADDRESS, register, value)
	return -1

def readACCx():
	acc_l = bus.read_byte_data(ACC_ADDRESS, LSM9DS1_OUT_X_L_XL)
	acc_h = bus.read_byte_data(ACC_ADDRESS, LSM9DS1_OUT_X_H_XL)
	
	acc_comb = (acc_l | acc_h << 8)
	
	return acc_comb if acc_comb < 32768 else acc_comb - 65536

def readACCy():
	acc_l = bus.read_byte_data(ACC_ADDRESS, LSM9DS1_OUT_Y_L_XL)
	acc_h = bus.read_byte_data(ACC_ADDRESS, LSM9DS1_OUT_Y_H_XL)

	acc_comb = (acc_l | acc_h << 8)

	return acc_comb if acc_comb < 32768 else acc_comb - 65536

def readACCz():
	
	acc_l = bus.read_byte_data(ACC_ADDRESS, LSM9DS1_OUT_Z_L_XL)
	acc_h = bus.read_byte_data(ACC_ADDRESS, LSM9DS1_OUT_Z_H_XL)

	acc_comb = (acc_l | acc_h << 8)
	
	return acc_comb if acc_comb < 32768 else acc_comb - 65536

def acc_init():
	writeACC(LSM9DS1_CTRL_REG5_XL, 0b01100111)
	writeACC(LSM9DS1_CTRL_REG6_XL, 0b00011000)

while True:

	acc_init()
	
	ACCx = readACCx()
	ACCy = readACCy()
	ACCz = readACCz()

	print ("***********")
	print ("X accel: %f G"%(ACCx*0.244/1000))
	print ("Y accel: %f G"%(ACCy*0.244/1000))
	print ("Z accel: %f G"%(ACCz*0.244/1000))
	
	time.sleep(0.5) #sample every half second
