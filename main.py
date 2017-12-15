#######################################################
# Team:         CCP2 (The Potato)
# Email:        candre1@umbc.edu
#               cu61692@umbc.edu
#               hash4@umbc.edu
#               wj1@umbc.edu
# File:         main.py
# Description:  This file serves as the main block for
#               the CCP code.  Uses peripheral files
#               to complete the system.
#######################################################

from packet_parser import *
from command_generator import *

## main ###############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simply takes "inString" and "outString"
#               and passes them into the function
#               "string_parser". (to be updated...)
#######################################################

def main():

    # RUN UNTIL SOMETHING STOPS ME
    #while (1):

    #GET LOCAL PTP STRING
    #localString = get_local_data(localPTPaddress)
    localString = "0010101010101010101010101010101010101010101010101010101010101011010101010101010101010101010101010101010101010101010101010110101101010101010101010101010101010101010101010101101011010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101"

    # SEND LOCAL PTP DATA
    #send_local_data(localString)

    # GET GUIDE PTP STRING
    #guideString = get_guide_data(WIFIaddress)
    guideString = "0110101010101010101010101010101010101010101010101010101010101011010101010101010101010101010101010101010101010101010101010110101101010101010101010101010101010101010101010101101011010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101"

    # USE TO SHOW PARSER FUNCTIONALITY
    #string_parser(localString, guideString)

    # USE "command_generator.py" AND "packet_parser.py" TO COMPARE DATA
    # AVEPTPFlag
    compareAvePtpFlag(getAvePtpFlag(guideString), getAvePtpFlag(localString))
    # LeaderFollowerFlag
    compareLeaderFolloweFlag(getLeaderFollowerFlag(guideString), getLeaderFollowerFlag(localString))
    # PositionInConvoy
    comparePositionInConvoy(getPositionInConvoy(guideString), getPositionInConvoy(localString))
    # EmergencyStop
    compareEmergencyStop(getEmergencyStop(guideString), getEmergencyStop(localString))
    # Location
    compareLocation(getLocation(guideString), getLocation(localString))
    # LineOfBearing
    compareLineOfBearing(getLineOfBearing(guideString), getLineOfBearing(localString))
    # VelocityX
    compareVelocityX(getVelocityX(guideString), getVelocityX(localString))
    # VelocityY
    compareVelocityY(getVelocityY(guideString), getVelocityY(localString))
    # VelocityZ
    compareVelocityZ(getVelocityZ(guideString), getVelocityZ(localString))
    # AccelerationX
    compareAccelerationX(getAccelerationX(guideString), getAccelerationX(localString))
    # AccelerationY
    compareAccelerationY(getAccelerationY(guideString), getAccelerationY(localString))
    # AccelerationZ
    compareAccelerationZ(getAccelerationZ(guideString), getAccelerationZ(localString))
    # ExtraData
    compareExtraData(getExtraData(guideString), getExtraData(localString))

main()
