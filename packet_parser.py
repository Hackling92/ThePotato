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
# Inputs:       string s
# Outputs:      N/A
# Description:  Parses the binary string given as input
#               and seperates the string into various
#               data based upon the decided string
#               format.
#######################################################
def string_parser(guideString, localString):
    
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

    # Calculate Controls
    #get_motor_commands(someInputs)


## main ###############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simply takes "inString" and "outString"
#               and passes them into the function
#               "string_parser". (to be updated...)
#######################################################

def main():
    #while (1):
    #outString = get_local_data(localPTPaddress)
    outString = "0010101010101010101010101010101010101010101010101010101010101011010101010101010101010101010101010101010101010101010101010110101101010101010101010101010101010101010101010101101011010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101"
    #send_local_data(outString)
    #inString = get_guide_data(WIFIaddress)
    inString = "0110101010101010101010101010101010101010101010101010101010101011010101010101010101010101010101010101010101010101010101010110101101010101010101010101010101010101010101010101101011010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101"
    string_parser(inString, outString)

main()
    
