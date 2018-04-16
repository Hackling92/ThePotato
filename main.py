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

# IMPORT
import os

### CCP ###
import socket
import time
from packet_parser import *
from command_generator import *
# For Vehicle GPIO
from motor_control import *
#import RPi.GPIO as GPIO                 # using Rpi.GPIO module
#from time import sleep                  # import function sleep for delay
#GPIO.setmode(GPIO.BOARD)                # GPIO numbering
#GPIO.setwarnings(False)                 # enable warning from GPIO

# OS DEPENDANT NETWORK
if(os.name != "nt"):
    from subprocess import check_output

### Bluetooth ###
import os
import bluetooth
import RPi.GPIO as GPIO
from bluetooth import *

# GLOBALS
BUFFER_SIZE = 1500
vehicleID = 0
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clients = []                            # used by leader for setup
leadCar = 0
startPressed = False
# set speed and delay
#RUNSPEED = 10
#DELAY = 2
#TURN = 8


## AVE_RECIEVE_PACKET #################################
# Inputs:       packetized data in as string
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def AVE_RECIEVE_PACKET(packetString):
    #add code here
    return 0

## AVE_CALCULATE_PACKET ###############################
# Inputs:       lead vehicle position data, drone position data
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def AVE_CALCULATE(leadVeh, drone):
    #add code here
    return 0

## AVE_SEND_PACKET ####################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def AVE_SEND_PACKET():
    #add code here
    return 0

## clientInList #######################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def clientInList(user):
    for client in clients:
        if(client == user):
            return client
    return 0

## sendUDP ############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def sendUDP(ip,port,message):
    s.sendto(message.encode('utf-8'), (ip,port))

## sendHeadToClient ###################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def sendHeadToClient():
    if(os.name == "nt"):
        ipAddr = socket.gethostnyname(socket.gethostname())
    else:
        ipAddr = str(check_output(["hostname", "-I"]))[2:-1].strip()
    if(len(clients) == 1):
        headClient = (ipAddr, 5555)
        sendUDP(clients[0][0], clients[0][1], str(headClient[0]) + ":" + str(headClient[1]))
        leadCar = ('',)
    for i in range(0,len(clients) - 1):
        sendUDP(clients[i + 1][0], clients[i + 1][1], str(clients[i][0]) + ":" + str(clients[i][1]))

## compare ############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compare(guideString,localString):
    # USE "command_generator.py" AND "packet_parser.py" TO COMPARE DATA
    compareAvePtpFlag(getAvePtpFlag(guideString), getAvePtpFlag(localString))
    compareLeaderFollowerFlag(getLeaderFollowerFlag(guideString), getLeaderFollowerFlag(localString))
    comparePositionInConvoy(getPositionInConvoy(guideString), getPositionInConvoy(localString))
    compareEmergencyStop(getEmergencyStop(guideString), getEmergencyStop(localString))
    compareLatitude(getLatitude(guideString), getLatitude(localString))
    compareLongitude(getLongitude(guideString), getLongitude(localString))
    compareLineOfBearing(getLineOfBearing(guideString), getLineOfBearing(localString))
    compareVelocityX(getVelocityX(guideString), getVelocityX(localString))
    compareVelocityY(getVelocityY(guideString), getVelocityY(localString))
    compareVelocityZ(getVelocityZ(guideString), getVelocityZ(localString))
    compareAccelerationX(getAccelerationX(guideString), getAccelerationX(localString))
    compareAccelerationY(getAccelerationY(guideString), getAccelerationY(localString))
    compareAccelerationZ(getAccelerationZ(guideString), getAccelerationZ(localString))
    # compareExtraData(getExtraData(guideString), getExtraData(localString))

## main ###############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Simply takes "inString" and "outString"
#               and passes them into the function
#               "string_parser". (to be updated...)
#######################################################
def main():

    # INITIAL SETUP
    global vehicleID
    global startPressed
    localString = "localString here"
    vehicleID = int(input("Vehicle ID Number: "))

    # FILEPATHS FOR READING DATA
    filepath = 'vehicle' + str(vehicleID) + ".txt"
    vehicleTxt = open(filepath, 'r')

    # SETUP DATA FOR TESTING
    vehicleTxt = vehicleTxt.readlines()

    # NETWORK SETUP (leader)
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

        # BEGIN OPERATION (leader)
        ### Bluetooth ###
        connection = False
        server_sock=BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)
        # Declare Port
        port = server_sock.getsockname()[1]
        # Unique UUID to connect with AVE Android Phone
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        # More setup
        advertise_service( server_sock, "AVECCPDataServer",
                service_id = uuid,
                service_classes = [ uuid, SERIAL_PORT_CLASS ],
                profiles = [ SERIAL_PORT_PROFILE ]						 )

        while (True):
            ### Bluetooth ###
            if(connection == False):
                print("Waiting for connection on RFCOMM channel %d" % port)
                client_sock, client_info = server_sock.accept()
                connection = True
                print("Accepted connection from ", client_info)
            try:
                data = client_sock.recv(1024)
                if (data == "disconnect"):
                    print("Client wanted to disconnect")
                    client_sock.close()
                    connection = False

                # this is the string that AVE is sending to RP3
                elif (data == "AVE test data!!"):
                    print ("The Android App just sent: %s" % data)
                    # Printing for testing
                    print ("Fake Data is being sent here!")
                    # this string is what RP3 sends to AVE
                    testTurning = "Value,"
                    testDirection = "Value,"
                    testSpeed = "Value,"
                    testDistance = "Value,"
                    testOffset = "Value"
                    testString = str(testTurning + testDirection + testSpeed + testDistance + testOffset)
                    # sends string to AVE
                    client_sock.send("RECEIVED: %s" % testString)
                    # Printing for testing
                    print("SENT: %s" % testString)

            except IOError:
                print("Connection disconnected!")
                client_sock.close()
                connection = False
                pass
            except BluetoothError:
                print("Something wrong with bluetooth")
                # this may have to be changed in the future
                # (it may be causing issues with continuous connection)
            except KeyboardInterrupt:
                print("\nDisconnected")
                client_sock.close()
                server_sock.close()
                break

            # put any processing data here
            # read sample data
            # Send data over WiFi
            for line in vehicleTxt:
                localString = line
                # prepare message to be sent
                message = s.recvfrom(BUFFER_SIZE)  # get location request
                if (str(message[0])[2:-1] == "getLocation"):
                    sendUDP(message[1][0], message[1][1], str(localString))
                    localString = line.strip().split(',')
                    print("\n--------------------------------------------------------------------")
                    print("Sending location data to: " + str(message[1]))
                    print("\tData: " + str(localString))
                    print("--------------------------------------------------------------------\n")
            print("End of sample PTP data reached, process will now exit.")
            break

    # NETWORK SETUP (follower)
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

            #####
            # THIS IS A TEMP INPUT THIS WILL BE REPLACED BY THE FLAG BIT IN THE PACKET
            # This idealy should be run on each loop iteration
            #####

            AVE_FLAG = str(input("AVE Y/N: "))
            if(AVE_FLAG.lower() == 'y'):
                AVE_FLAG = 1
            else:
                AVE_FLAG = 0

            #####
            # END TEMP CODE
            #####

        # CCP2 CODE
        # NOTE: this needs to be refactored to use something like recieve calc and send
        if (not AVE_FLAG):
                        # BREAKS ON INTERRUPT
            try:
                # BEGIN OPERATION (follower)
                speed = 0 # initial speed
                while (True):
                    for line in vehicleTxt:
                        localString = line.strip().split(',') # local ptp data from file
                        sendUDP(leadCar[0], leadCar[1], "getLocation")  # ask for location from lead car
                        message = s.recvfrom(BUFFER_SIZE) # message received from guide car
                        guideString = str(message[0])[2:-1] # guideString obtained
                        guideString = guideString.strip("\\n").split(',')
                        # calculate the offsets for the data and print them here
                        # drive commands can be formed here as well
                        print("\n--------------------------------------------------------------------")
                        print("Local PTP Data: " + str(localString))
                        print("Guide PTP Data: " + str(guideString))
                        print("Calculated Offsets:")
                        #speed = calculateSkid(guideString, localString, speed)
                        compare(guideString, localString)
                        print("--------------------------------------------------------------------")

                        time.sleep(0.5)   # add artificial delay so test dosnt run to fast to be boring

                    print("End of sample PTP data reached, process will now exit.")
                    fullStop()
                    break

            # MOTOR SHUTOFF
            except Exception as e:
                    fullStop()
                    print(e)


        # AVE CODE HERE
        else:
            # Modify these as you see fit the function definitions are included above
            AVE_RECIEVE_PACKET(packetString) # possibly using your bluetooth
            AVE_CALCULATE(leadVeh, drone) # extra math for z axis if needed
            AVE_SEND_PACKET() # possibly using your bluetooth

main()
s.close()
