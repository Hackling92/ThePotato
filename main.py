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

import socket
import time
from packet_parser import *
from command_generator import *


# CONSTANTS
BUFFER_SIZE = 1500

# GLOBALS
vehicleID = 0
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clients = []    # used by leader for setup
leadCar = 0
startPressed = False


def clientInList(user):
    for client in clients:
        if(client == user):
            return client
    return 0

def sendUDP(ip,port,message):
    s.sendto(message.encode('utf-8'), (ip,port))


def sendHeadToClient():

    if(len(clients) == 1):
        headClient = (socket.gethostbyname(socket.gethostname()), 5555)
        sendUDP(clients[0][0], clients[0][1], str(headClient[0]) + ":" + str(headClient[1]))
        leadCar = ('',)
    for i in range(0,len(clients) - 1):
        sendUDP(clients[i + 1][0], clients[i + 1][1], str(clients[i][0]) + ":" + str(clients[i][1]))


def compare(guideString,localString):
    # USE "command_generator.py" AND "packet_parser.py" TO COMPARE DATA
    # AVEPTPFlag
    compareAvePtpFlag(getAvePtpFlag(guideString), getAvePtpFlag(localString))
    # LeaderFollowerFlag
    compareLeaderFollowerFlag(getLeaderFollowerFlag(guideString), getLeaderFollowerFlag(localString))
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

    global vehicleID
    global startPressed

    localString = "localString here"

    vehicleID = int(input("Vehicle ID Number: "))

    # FILEPATHS FOR READING DATA
    filepath = 'vehicle' + str(vehicleID) + ".txt"
    vehicleTxt = open(filepath, 'r')

    # SETUP DATA FOR TESTING
    vehicleTxt = vehicleTxt.readlines()

    if (vehicleID == 1):
        print("I am leader for convoy.")
        print("Waiting for vehicles to connect.\n")
        s.bind(("", 5555))
        isSetup = False
        while (not isSetup):
            message = s.recvfrom(BUFFER_SIZE)
            if (clientInList(message[1])):
                # check to see if message is start
                if (str(message[0])[2:-1] == "start"):  # a vehicle requested to start run
                    isSetup = True
                    sendHeadToClient()
            else:
                clients.append(message[1])
                print("Added vehicle to convoy at:", message[1])
                print("Updated client list:")
                print("\t", clients)

        while (True):
            # put any processing data here

            for line in vehicleTxt:
                localString = line.strip().split(',')

                message = s.recvfrom(BUFFER_SIZE)  # get location request
                if (str(message[0])[2:-1] == "getLocation"):
                    sendUDP(message[1][0], message[1][1], str(localString))
                    print("\n--------------------------------------------------------------------")
                    print("Sending location data to: " + str(message[1]))
                    print("\tData: " + str(localString))
                    print("--------------------------------------------------------------------\n")
            print("End of sample PTP data reached, process will now exit.")
            break


    else:
        print("Follower Number", (vehicleID - 1))
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sendUDP("<broadcast>", 5555, "client" + str(vehicleID))
        while (True):
            if (startPressed == 'y'):
                sendUDP("<broadcast>", 5555, "start")
                recData = s.recvfrom(BUFFER_SIZE)  # get your leader and save it
                leadAdd, leadPort = str(recData[0])[2:-1].split(':')
                leadCar = (leadAdd, int(leadPort))
                print("Connected to convoy.")
                print("\tGot guide vehicle at:",leadCar)
                break
            startPressed = str(input("Start run (y,n): "))
            # need parallel code here to check if packet start came in
        while (True):

            for line in vehicleTxt:
                localString = line.strip().split(',') # local ptp data from fil

                sendUDP(leadCar[0], leadCar[1], "getLocation")  # ask for location from lead car
                message = s.recvfrom(BUFFER_SIZE) # message received from guide car
                guideString = str(message[0])[2:-1] # guideString obtained

                # calculate the offsets for the data and print them here
                # drive commands can be formed here aswell
                print("\n--------------------------------------------------------------------")
                print("Local PTP Data: " + str(localString))
                print("Guide PTP Data: " + str(guideString))
                print("Calculated Offsets:")
                print("\tBlah blah, blah")
                print("--------------------------------------------------------------------\n")

                time.sleep(3)   # add artificial delay so test dosnt run to fast to be boring

            print("End of sample PTP data reached, process will now exit.")
            break












"""
    # FILEPATHS FOR READING DATA
    filepath = 'vehicle' + str(vehicleID) + ".txt"
    vehicleTxt = open(filepath, 'r')

    # SETUP DATA FOR TESTING
    vehicleTxt = vehicleTxt.readlines()
    sample = 1

    # RUN UNTIL SOMETHING STOPS ME
    #while(1):
    for line in vehicleTxt:

        # PRINT CURRENT SAMPLE (TESTING)
        #print("SAMPLE: " + str(sample) + " ====================================")
        localString = vehicleTxt[sample-1].strip().split(',')
        #print(localString)
        #compare(guideString,localString)
        # INCREMENT SAMPLE VALUE (TESTING)
        sample += 1

"""


main()
s.close()