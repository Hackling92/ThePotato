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
def string_parser(s):
    
    # Separate Location Data
    AvePtpFlag = s[0]
    LeaderFollowerFlag = s[1]
    PositionInConvoy = s[2:81]
    EmergencyStop = s[82]
    Location = s[83:112]
    LineOfBearing = s[113:128]
    VelocityX = s[129:160]
    VelocityY = s[161:192]
    VelocityZ = s[193:224]
    AccelerationX = s[225:256]
    AccelerationY = s[257:288]
    AccelerationZ = s[289:320]
    extraData = s[321:]

    # Print Data
    print(AvePtpFlag)
    print(LeaderFollowerFlag)
    print(PositionInConvoy)
    print(EmergencyStop)
    print(Location)
    print(LineOfBearing)
    print(VelocityX)
    print(VelocityY)
    print(VelocityZ)
    print(AccelerationX)
    print(AccelerationY)
    print(AccelerationZ)
    print(extraData)


## main ###############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simply takes "inString" and passes it
#               int0 the function "string_parser".
#               (to be updated...)
#######################################################
def main():
    inString = "1010101010101010101010101010101010101010101010101010101010101011010101010101010101010101010101010101010101010101010101010110101101010101010101010101010101010101010101010101101011010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101"
    string_parser(inString)

main()
    
