import PTP
import time

PTPi = PTP.PTP()

while True:

	PTPi.predict_update()

	rlat,rlon,rbrg,rvel = PTPi.raw_read()

	klat,klon,kbrg,kvel = PTPi.ptp_read()

	print(" ")
	print("MEASURED:")
	print("LAT: %f"%rlat)
	print("LON: %f"%rlon)
	print("BRG: %f"%rbrg)
	print("VEL: %f"%rvel)
	print(" ")
	print("KALMAN:")
	print("LAT: %f"%klat)
	print("LON: %f"%klon)
	print("BRG: %f"%kbrg)
	print("VEL: %f"%kvel)
	print(" ")

	time.sleep(0.5)

    
