#######################################################
# Team:         CCP2 (The Potato)
# Email:        candre1@umbc.edu
#               cu61692@umbc.edu
#               hash4@umbc.edu
#               wj1@umbc.edu
# File:         packet_parser.py
# Description:  This file will be used to obtain data
#               sent to the CCP unit from the PTP or
#               AVE unit
#######################################################

## getPacket ##########################################
# Inputs:       string dataString
# Outputs:      N/A
# Description:  Parses the binary string given as input
#               and separates the string into various
#               data based upon the decided string
#               format.
#######################################################
def getPacket(dataString):

    # Separate Data
    AvePtpFlag = dataString[0]
    LeaderFollowerFlag = dataString[1]
    PositionInConvoy = dataString[2]
    EmergencyStop = dataString[3]
    Latitude = dataString[4]
    Longitude = dataString[5]
    LineOfBearing = dataString[6]
    VelocityX = dataString[7]
    VelocityY = dataString[8]
    VelocityZ = dataString[9]
    AccelerationX = dataString[10]
    AccelerationY = dataString[11]
    AccelerationZ = dataString[12]

    # Print Data
    print("AvePtpFlag: " + AvePtpFlag)
    print("LeaderFollowerFlag: " + LeaderFollowerFlag)
    print("PositionInConvoy: " + PositionInConvoy)
    print("EmergencyStop: " + EmergencyStop)
    print("Latitude: " + Latitude)
    print("Longitude: " + Longitude)
    print("LineOfBearing: " + LineOfBearing)
    print("VelocityX: " + VelocityX)
    print("VelocityY: " + VelocityY)
    print("VelocityZ: " + VelocityZ)
    print("AccelerationX: " + AccelerationX)
    print("AccelerationY: " + AccelerationY)
    print("AccelerationZ: " + AccelerationZ)

## getAvePtpFlag ######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getAvePtpFlag(dataString):
	return dataString[0]

## getLeaderFollowerFlag ##############################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getLeaderFollowerFlag(dataString):
	return dataString[1]

## getPositionInConvoy ################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getPositionInConvoy(dataString):
	return dataString[2]

## getEmergencyStop ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getEmergencyStop(dataString):
	return dataString[3]

## getLatitude ########################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getLatitude(dataString):
	return float(dataString[4])

## getLongitude #######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getLongitude(dataString):
        return float(dataString[5])

## getLineOfBearing ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getLineOfBearing(dataString):
	return int(dataString[6])

## getVelocityX #######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getVelocityX(dataString):
	return float(dataString[7])

## getVelocityY #######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getVelocityY(dataString):
	return float(dataString[8])

## getVelocityZ #######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getVelocityZ(dataString):
	return float(dataString[9])

## getAccelerationX ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getAccelerationX(dataString):
	return dataString[10]

## getAccelerationY ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getAccelerationY(dataString):
	return dataString[11]

## getAccelerationZ ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getAccelerationZ(dataString):
	return dataString[12]

## getExtraData #######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getExtraData(dataString):
	return dataString[13]

