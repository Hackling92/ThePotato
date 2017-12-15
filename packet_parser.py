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

## string_parser ######################################
# Inputs:       string localString, string guideString
# Outputs:      N/A
# Description:  Parses the binary string given as input
#               and separates the string into various
#               data based upon the decided string
#               format.
#######################################################
def string_parser(localString, guideString):

    # Separate Guide Data
    GuideAvePtpFlag = guideString[0]
    GuideLeaderFollowerFlag = guideString[1]
    GuidePositionInConvoy = guideString[2:81]
    GuideEmergencyStop = guideString[82]
    GuideLocation = guideString[83:112]
    GuideLineOfBearing = guideString[113:128]
    GuideVelocityX = guideString[129:160]
    GuideVelocityY = guideString[161:192]
    GuideVelocityZ = guideString[193:224]
    GuideAccelerationX = guideString[225:256]
    GuideAccelerationY = guideString[257:288]
    GuideAccelerationZ = guideString[289:320]
    GuideExtraData = guideString[321:]

    # Separate Local Data
    LocalAvePtpFlag = localString[0]
    LocalLeaderFollowerFlag = localString[1]
    LocalPositionInConvoy = localString[2:81]
    LocalEmergencyStop = localString[82]
    LocalLocation = localString[83:112]
    LocalLineOfBearing = localString[113:128]
    LocalVelocityX = localString[129:160]
    LocalVelocityY = localString[161:192]
    LocalVelocityZ = localString[193:224]
    LocalAccelerationX = localString[225:256]
    LocalAccelerationY = localString[257:288]
    LocalAccelerationZ = localString[289:320]
    LocalExtraData = localString[321:]

    # Print Data
    print("GuideAvePtpFlag: " + GuideAvePtpFlag)
    print("LocalAvePtpFlag: " + LocalAvePtpFlag)
    print("GuideLeaderFollowerFlag: " + GuideLeaderFollowerFlag)
    print("LocalLeaderFollowerFlag: " + LocalLeaderFollowerFlag)
    print("GuidePositionInConvoy: " + GuidePositionInConvoy)
    print("LocalPositionInConvoy: " + LocalPositionInConvoy)
    print("GuideEmergencyStop: " + GuideEmergencyStop)
    print("LocalEmergencyStop: " + LocalEmergencyStop)
    print("GuideLocation: " + GuideLocation)
    print("LocalLocation: " + LocalLocation)
    print("GuideLineOfBearing: " + GuideLineOfBearing)
    print("LocalLineOfBearing: " + LocalLineOfBearing)
    print("GuideVelocityX: " + GuideVelocityX)
    print("LocalVelocityX: " + LocalVelocityX)
    print("GuideVelocityY: " + GuideVelocityY)
    print("LocalVelocityY: " + LocalVelocityY)
    print("GuideVelocityZ: " + GuideVelocityZ)
    print("LocalVelocityZ: " + LocalVelocityZ)
    print("GuideAccelerationX: " + GuideAccelerationX)
    print("LocalAccelerationX: " + LocalAccelerationX)
    print("GuideAccelerationY: " + GuideAccelerationY)
    print("LocalAccelerationY: " + LocalAccelerationY)
    print("GuideAccelerationZ: " + GuideAccelerationZ)
    print("LocalAccelerationZ: " + LocalAccelerationZ)
    print("GuideExtraData: " + GuideExtraData)
    print("LocalExtraData: " + LocalExtraData)


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
	return dataString[2:81]

## getEmergencyStop ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getEmergencyStop(dataString):
	return dataString[82]

## getLocation ########################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getLocation(dataString):
	return dataString[83:112]

## getLineOfBearing ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getLineOfBearing(dataString):
	return dataString[113:128]

## getVelocityX #######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getVelocityX(dataString):
	return dataString[129:160]

## getVelocityY #######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getVelocityY(dataString):
	return dataString[161:192]

## getVelocityZ #######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getVelocityZ(dataString):
	return dataString[193:224]

## getAccelerationX ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getAccelerationX(dataString):
	return dataString[225:256]

## getAccelerationY ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getAccelerationY(dataString):
	return dataString[257:288]

## getAccelerationZ ###################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getAccelerationZ(dataString):
	return dataString[289:320]

## getExtraData #######################################
# Inputs:       string dataString
# Outputs:      Specific location data (size varies)
# Description:  Parses the binary string given as input
#               and selects specific data depending on
#               the function that is called.
#######################################################
def getExtraData(dataString):
	return dataString[321:]

