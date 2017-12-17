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

def compare(guideString,localString):
    # USE "command_generator.py" AND "packet_parser.py" TO COMPARE DATA
    # AVEPTPFlag
    compareAvePtpFlag(getAvePtpFlag(guideString), getAvePtpFlag(localString))
    # LeaderFollowerFlag
    compareLeaderFolloweFlag(getLeaderFollowerFlag(guideString), getLeaderFollowerFlag(localString))
    # PositionInConvoy
    comparePositionInConvoy(getPositionInConvoy(guideString), getPositionInConvoy(localString))
    # EmergencyStop
    compareEmergencyStop(getEmergencyStop(guideString), getEmergencyStop(localString))
    # Latitude
    compareLatitude(getLatitude(guideString), getLatitude(localString))
    # Longitude
    compareLongitude(getLongitude(guideString), getLongitude(localString))
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
    # compareExtraData(getExtraData(guideString), getExtraData(localString))


## main ###############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simply takes "inString" and "outString"
#               and passes them into the function
#               "string_parser". (to be updated...)
#######################################################

def main():

    # FILEPATHS FOR READING DATA
    filepath1 = 'leader1.txt'
    filepath2 = 'follower1.txt'
    guideTxt = open(filepath1, 'r')
    localTxt = open(filepath2, 'r')

    # SETUP DATA FOR TESTING
    guideTxt = guideTxt.readlines()
    localTxt = localTxt.readlines()
    sample = 1

    # RUN UNTIL SOMETHING STOPS ME
    #while(1):
    for line in localTxt:

        # PRINT CURRENT SAMPLE (TESTING)
        print("SAMPLE: " + str(sample) + " ====================================")

        # READ IN CURRENT DATA
        guideString = guideTxt[0].strip()
        localString = localTxt[0].strip()
        guideString = guideString.split(',')
        localString = localString.split(',')

        #GET LOCAL PTP STRING
        #localString = get_local_data(localPTPaddress)
        #localString = "0010101010101010101010101010101010101010101010101010101010101011010101010101010101010101010101010101010101010101010101010110101101010101010101010101010101010101010101010101101011010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101"

        # SEND LOCAL PTP DATA
        #send_local_data(localString)

        # GET GUIDE PTP STRING
        #guideString = get_guide_data(WIFIaddress)
        #guideString = "0110101010101010101010101010101010101010101010101010101010101011010101010101010101010101010101010101010101010101010101010110101101010101010101010101010101010101010101010101101011010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101"

        compare(guideString,localString)

        # INCREMENT SAMPLE VALUE (TESTING)
        sample += 1

main()
