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
import RPi.GPIO as GPIO                 # using Rpi.GPIO module
#from time import sleep                 # import function sleep for delay
GPIO.setmode(GPIO.BOARD)                # GPIO numbering
GPIO.setwarnings(False)                 # enable warning from GPIO

# OS DEPENDANT NETWORK
if(os.name != "nt"):
    from subprocess import check_output

### Bluetooth ###
import os
import bluetooth
#import RPi.GPIO as GPIO
from bluetooth import *

### GLOBALS ###
# AVE
USING_AVE = False 			#FLAG used to set CCP to AVE or iRobot mode
AVE_TEST = False
# PTP
USING_PTP = False			#FLAG used to switch between PTP or test data
if (USING_PTP):
    import PTP
    ptpi = PTP.PTP()
    print("Waiting 60sec for filter")
    count = 0
    while(count < 20):
        ptpi.predict_update()
        time.sleep(0.5)
        count += 1
        print("Time Count:", count)
PTP_TEST = True 			#FLAG used to show test print for PTP data
# network
BUFFER_SIZE = 1500
vehicleID = 0
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
clients = []                            # used by leader for setup
leadCar = 0
startPressed = False
# control panel
DEBOUNCE_INTERVAL = 150
inputPins = [33,22,12,32]
outputPins = [11,13,15,19,21,23,29,31,35,37,40,38,36]
buttons = {1: 33, 2: 22, 3: 12, 4: 32}
global selCnt
global join
global operate
global localPress
selCnt = 1
join = 0
operate = 0
localPress = False
leftTestData = ['0','1','7','u','n']
rightTestData = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

### Display Tebles ###
segToPin = {'la': 15, 'lb': 19, 'lc': 35, 'ld': 13, 'le': 31, 'lf': 11, 'ra': 23, 'rb': 29, 'rc': 36, 'rd': 40, 're': 37, 'rf': 21, 'rg': 38}
disp = {'left':{'0': [segToPin['la'],segToPin['lb'],segToPin['lc'],segToPin['ld'],segToPin['le'],segToPin['lf']],
                '1': [segToPin['lb'],segToPin['lc']],
                '7': [segToPin['la'],segToPin['lb'],segToPin['lc']],
                'u': [segToPin['lb'],segToPin['lc'],segToPin['ld'],segToPin['le'],segToPin['lf']],
                'n': [segToPin['la'],segToPin['lb'],segToPin['lc'],segToPin['le'],segToPin['lf']],
                'blank': [segToPin['la'],segToPin['lb'],segToPin['lc'],segToPin['ld'],segToPin['le'],segToPin['lf']]},
        'right':{'0': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf']],
                '1': [segToPin['rb'],segToPin['rc']],
                '2': [segToPin['ra'],segToPin['rb'],segToPin['rd'],segToPin['re'],segToPin['rg']],
                '3': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['rg']],
                '4': [segToPin['rb'],segToPin['rc'],segToPin['rf'],segToPin['rg']],
                '5': [segToPin['ra'],segToPin['rc'],segToPin['rd'],segToPin['rf'],segToPin['rg']],
                '6': [segToPin['ra'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                '7': [segToPin['ra'],segToPin['rb'],segToPin['rc']],
                '8': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                '9': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rf'],segToPin['rg']],
                'a': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                'b': [segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                'c': [segToPin['ra'],segToPin['rd'],segToPin['re'],segToPin['rf']],
                'd': [segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rg']],
                'e': [segToPin['ra'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                'f': [segToPin['ra'],segToPin['re'],segToPin['rf'],segToPin['rg']],
                'blank': [segToPin['ra'],segToPin['rb'],segToPin['rc'],segToPin['rd'],segToPin['re'],segToPin['rf'],segToPin['rg']]}}

## printSegment #######################################
# pos is left right or both displays
# left character (0,1,7,u,n)
# right character (0-9, a-f)
#######################################################
def printSegment(pos, char):
    if(pos == 'both'):
        GPIO.output(disp['left']['blank'], GPIO.LOW)
        GPIO.output(disp['right']['blank'], GPIO.LOW)
        GPIO.output(disp['left'][char[0]], GPIO.HIGH)
        GPIO.output(disp['right'][char[1]], GPIO.HIGH)
    elif(pos == 'left'):
        GPIO.output(disp['left']['blank'], GPIO.LOW)
        GPIO.output(disp['left'][char], GPIO.HIGH)
    elif(pos == 'right'):
        GPIO.output(disp['right']['blank'], GPIO.LOW)
        GPIO.output(disp['right'][char], GPIO.HIGH)

## selectUp ###########################################
# Inputs:       channel
# Outputs:	N/A
# Description:	
#######################################################
def selectUp(channel):
    global selCnt
    global join
    if(join == False):
        selCnt = (selCnt + 1) % 16
    if(selCnt == 0):
        selCnt = 1
    if(selCnt < 10):
        printSegment('both', "0" + str(selCnt))
    else:
        printSegment('both', "1" + str(selCnt - 10))

## selectDown #########################################
# Inputs:       channel
# Outputs:      N/A
# Description:  
#######################################################
def selectDown(channel):
    global selCnt
    global join
    if(join == False):
        selCnt = (selCnt - 1) % 16
    if(selCnt == 0):
        selCnt = 15
    if(selCnt < 10):
        printSegment('both', "0" + str(selCnt))
    else:
        printSegment('both', "1" + str(selCnt - 10))


## beginOP ############################################
# Inputs:       channel
# Outputs:      N/A
# Description:  
#######################################################
def beginOp(channel):
    #print("Begin Operation Pressed")
    global join
    global operate
    if (join == False):
        join = True
    elif (join == True):
        sendUDP("192.168.0.1", 5555, "start")
        localPress = True	
        operate = True


## haltOp #############################################
# Inputs:       channel
# Outputs:      N/A
# Description:  
#######################################################
def haltOp(channel):
    print("Halt Operation Pressed")
    global operate
    operate = False
    sendStopMessage()

## AVE_RECIEVE_PACKET #################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  AVE function stubs for convenience of
#               translation to AVE commands.
#               (future implementation?)
#######################################################
def AVE_RECIEVE_PACKET(packetString):
    #add code here
    return 0

## AVE_CALCULATE_PACKET ###############################
# Inputs:       N/A
# Outputs:      N/A
# Description:  N/A
#######################################################
def AVE_CALCULATE(leadVeh, drone):
    #add code here
    return 0

## AVE_SEND_PACKET ####################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  N/A
#######################################################
def AVE_SEND_PACKET():
    #add code here
    return 0

## clientInList #######################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  N/A
#######################################################
def clientInList(user):
    for client in clients:
        if(client == user):
            return client
    return 0

## sendUDP ############################################
# Inputs:       ip, port, message
# Outputs:      N/A
# Description:  Sends a UDP packet to the inputted IP
#               and port. Packet contains the input
#               message.
#######################################################
def sendUDP(ip,port,message):
    #print("\n\nUDP MESSAGE SENT: ", message)
    #print("\tDEST IP:",ip)
    #print("\tDEST PORT:",port,"\n\n")
    s.sendto(message.encode('utf-8'), (ip,port))

## sendHeadToClient ###################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Additional setup for WiFi network.
#               Sends host IP to clients that wish to
#               join.
#######################################################
def sendHeadToClient():
    if(os.name == "nt"):
        ipAddr = socket.gethostbyname(socket.gethostname())
    else:
        ipAddr = str(check_output(["hostname", "-I"]))[2:-1].strip()
    #if(len(clients) == 1):
    headClient = (ipAddr, 5555)
    sendUDP(clients[0][0], clients[0][1], str(headClient[0]) + ":" + str(headClient[1]))
    leadCar = ('',)
    for i in range(0,len(clients) - 1):
        sendUDP(clients[i + 1][0], clients[i + 1][1], str(clients[i][0]) + ":" + str(clients[i][1]))

def sendStartToClient():
    for i in range(0,len(clients)):
        sendUDP(clients[i][0], clients[i][1], str("start"))


def sendStopMessage():
    for i in range(0,len(clients)):
        sendUDP(clients[i][0],clients[i][1], "stop")

## compare ############################################
# Inputs:       guideString, localString
# Outputs:      N/A
# Description:  Generic compare of all GPS data. Used
#               primarily for testing purposes.
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
    #compareExtraData(getExtraData(guideString), getExtraData(localString))

## main ###############################################
# Inputs:       N/A
# Outputs:      N/A
# Description:  Begins by setting up network based on
#               user input. Then when start is pressed
#               begins sending or receiving data
#               dependant upon whether the local unit
#               is assigned as leader or follower.
#######################################################
def main():

    global operate
    global join
    global selCnt

    # CONTROL PANEL SETUP
    GPIO.setup(outputPins, GPIO.OUT) # set all led pins as outputs
    GPIO.setup(inputPins, GPIO.IN, pull_up_down = GPIO.PUD_UP) # set all buttons as inputs with pullup resistors
    GPIO.output(disp['left']['blank'], GPIO.LOW)    # clear any old segments
    GPIO.output(disp['right']['blank'], GPIO.LOW)   # clear any old segments
    GPIO.add_event_detect(buttons[1], GPIO.FALLING, callback=selectUp, bouncetime=DEBOUNCE_INTERVAL)
    GPIO.add_event_detect(buttons[2], GPIO.FALLING, callback=selectDown, bouncetime=DEBOUNCE_INTERVAL)
    GPIO.add_event_detect(buttons[3], GPIO.FALLING, callback=beginOp, bouncetime=600)
    GPIO.add_event_detect(buttons[4], GPIO.FALLING, callback=haltOp, bouncetime=DEBOUNCE_INTERVAL)

    printSegment('both', "01")

    # INITIAL NETWORK SETUP
    global vehicleID
    global startPressed
    global localPress
    localString = "localString here"
    #vehicleID = int(input("Vehicle ID Number: "))
    print("Please enter vehicle ID...")
    while(join == False):
        vehicleID = selCnt

    print("GOT ID: " + str(vehicleID))

    # FILEPATHS FOR READING DATAv
    if (vehicleID == 1):
        filepath = "guidesim1.txt"
    else:
        filepath = "localsim1.txt"
    vehicleTxt = open(filepath, 'r')

    # SETUP DATA FOR TESTING
    vehicleTxt = vehicleTxt.readlines()

    # NETWORK SETUP (leader)
    if (vehicleID == 1):
        print("I am leader for convoy.")
        print("Waiting for vehicles to connect.\n")
        s.bind(("", 5555))
        operate = False
        while (not operate):
            message = s.recvfrom(BUFFER_SIZE)
            if (clientInList(message[1])):
                # check to see if message is start
                if (str(message[0])[2:-1] == "start"):  # a vehicle requested to start run
                    print("Got start from slave")
                    sendStartToClient()
                    time.sleep(1)
                    operate = True
                    sendHeadToClient()
            else:
                clients.append(message[1])
                print("Added vehicle to convoy at:", message[1])
                print("Updated client list:")
                print("\t", clients)

        # BEGIN OPERATION (leader)
        while (operate):

            # read sample data from file and send data over network
            if (not USING_PTP):
                for line in vehicleTxt:
                    #print (gps.gpsread())
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
                    elif(str(message[0])[2:-1] == "stop"):
                        operate = False
                        break
                #print("End of sample PTP data reached, process will now exit.")
                break
            # Pulls PTP data and sends over network
            else:
                if (PTP_TEST):
                    print("Acquiring PTP Data...")
#               localString = gps.gpsread()
                ptpi.predict_update()
                lat,lon,brg,vel = ptpi.ptp_read()
                localString = "%s,%s,%s,%s"%(str(lat),str(lon),str(brg),str(vel))
                print(localString)
                message = s.recvfrom(BUFFER_SIZE)
                if (str(message[0])[2:-1] == "getLocation"):
                    sendUDP(message[1][0], message[1][1], str(localString))
                    localString = localString.strip().split(',')
                    print("\n--------------------------------------------------------------------")
                    print("Sending location data to: " + str(message[1]))
                    print("\tData: " + str(localString))
                    print("--------------------------------------------------------------------\n")
                elif(str(message[0])[2:-1] == "stop"):
                    operate = False
                    break

    # NETWORK SETUP (follower)
    else:

        ### WiFi ###
        print("Follower Number", (vehicleID - 1))
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sendUDP("<broadcast>", 5555, "client" + str(vehicleID))
        print("Waiting for start button press...")
        operate = False
        if(localPress == False):
            message = s.recvfrom(BUFFER_SIZE) # get start packet from remote
            if(str(message[0])[2:-1] == "start"):
                operate = True
                print("Got remote start packet")
            else:
                print("ERROR: Got unknown packet in remote start")
                print("\tData Was:",str(message[0])[2:-1])
        while (True):
            if (operate):
                recData = s.recvfrom(BUFFER_SIZE)  # get your leader and save it
                leadAdd, leadPort = str(recData[0])[2:-1].split(':')
                leadCar = (leadAdd, int(leadPort))
                print("Connected to convoy.")
                print("\tGot guide vehicle at:",leadCar)
                break


        ### AVE ###
        #AveFlag = str(input("AVE Unit? (y,n): "))
        AveFlag = USING_AVE
        if (AveFlag):
            #AveFlag = True
            BTconnection = False
            while (BTconnection == False):
                server_sock=BluetoothSocket( RFCOMM )
                server_sock.bind(("",PORT_ANY))
                server_sock.listen(1)
                port = server_sock.getsockname()[1]
                # unique UUID to connect with AVE Android Phone
                uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
                #file = open("vehicle3.txt", "r")
                advertise_service(server_sock, "AVECCPDataServer",
                                  service_id = uuid,
                                  service_classes = [ uuid, SERIAL_PORT_CLASS ],
                                  profiles = [ SERIAL_PORT_PROFILE ])

                while (operate):
                    # Confirm BT if set to AVE mode
#                    if (AveFlag):
#                        if(BTconnection == False):
#                            print("Waiting for connection on RFCOMM channel %d" % port)
#                            client_sock, client_info = server_sock.accept()
#                            BTconnection = True
#                            print("Accepted connection from ", client_info)

                    # BREAKS ON INTERRUPT
                    try:
                        # BEGIN OPERATION (follower)
                        speed = 0 # initial speed
                        testCount = 0 # for AVE_TEST
                        while (True):
                            ### CCP TO AVE ###
                            sendUDP(leadCar[0], leadCar[1], "getLocation")  # ask for location from lead car
                            message = s.recvfrom(BUFFER_SIZE) # message received from guide car
                            # if a stop signal is received stop the convoy
                            if(str(message[0])[2:-1] == "stop"):
                                operate = False
                                break
                                guideString = str(message[0])[2:-1] # guideString obtained
                            guideString = guideString.strip("\\n").split(',')
                            # Get GPS data from AVE
#                           localString = client_sock.recv(1024)
                            localString = "b'39.11,79.11,20,1.4'"
                            localString = str(localString[2:-1])
                            localString = localString.strip("\\n").split(',')
                            ### AVE TO CCP
                            if (AVE_TEST):
                                localString = vehicleTxt.readlines()
                                testCount += 1
                            turning = calculateBearing(guideString, localString)
                            direction = calculateDir(guideString, localString)
                            speed = calculateSpeed(guideString, localString, speed)
                            distance = calculateDist(guideString, localString)
                            offset = str(0)
                            aline = str(turning) + "," + str(direction) + "," + str(speed) + "," + str(distance) + "," + str(offset)
#                           client_sock.send(aline);
                            print("String that was just sent: %s" % aline)
                            ### AVE TO CCP ###

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
                    server_sock.close()

        ### iROBOT ###
        else:
            try:
                while (operate):
                    speed = 0
                    if (not USING_PTP):
                        count = 0
                        for line in vehicleTxt:
                            count +=1
                            #print("ERROR: Line Number", count)
                            localString = line.strip().split(',') # local ptp data from file
                            sendUDP(leadCar[0], leadCar[1], "getLocation")  # ask for location from lead car
                            message = ["b'getLocation'",""] # prime the while loop
                            while(str(message[0])[2:-1] == "stop" or str(message[0])[2:-1] == "getLocation"):
                                #print("IN LOOP MESSAGE: ",message[0])
                                message = s.recvfrom(BUFFER_SIZE) # message received from guide car
                                #print("\n\nGUIDE CAR SENT:\n\t",message[0],"\n\n")
                                # if a stop signal is received stop the convoy
                                if(str(message[0])[2:-1] == "stop"):
                                    operate = False
                                    #sendUDP("<broadcast>",5555,"stop")
                                    break
                                elif(str(message[0])[2:-1] == "getLocation"):
                                    sendUDP(message[1][0], int(message[1][1]), str(line))
                                    print("\n---------------------------------------------------------------")
                                    print("Sending location data to: " + str(message[1]))
                                    print("\tData: " + str(line))
                                    print("-----------------------------------------------------------------\n")
                                else:
                                    guideString = str(message[0])[2:-1] # guideString obtained
                                    guideString = guideString.strip("\\n").split(',')
                                    # calculate the offsets for the data and print them here
                                    # drive commands can be formed here as well
                                    print("\n-----------------------------------------------------------------")
                                    #print("Local PTP Data: " + str(localString))
                                    #print("Guide PTP Data: " + str(guideString))
                                    print("GPS DATA:")
                                    print("Guide Latitude: ", getLatitude(guideString))
                                    print("Local Latitude: ", getLatitude(localString))
                                    print("Guide Longitude: ", getLongitude(guideString))
                                    print("Local Longitude: ", getLongitude(localString))
                                    print("Guide Line of Bearing: ", getLineOfBearing(guideString))
                                    print("Local Line of Bearing: ", getLineOfBearing(localString))
                                    print("Guide Velocity: ", getVelocity(guideString))
                                    print("Local Velocity: ", getVelocity(localString))
                                    print("----------------------")
                                    speed = calculateSkid(guideString, localString, speed)
                                    #compare(guideString, localString)
                                    print("-------------------------------------------------------------------")
                                    if(operate == False):
                                        break;
                            time.sleep(0.5)   # add artificial delay so test dosnt run to fast to be boring
                            if(operate == False):
                                break;
                        print("End of sample PTP data reached, process will now exit.")
                        fullStop()
                        break
                    else:
                        while(operate):
                            if (PTP_TEST):
                                print("Acquiring PTP Data...")
                            ptpi.predict_update()
                            lat,lon,brg,vel = ptpi.ptp_read()
                            localString = "%s,%s,%s,%s"%(str(lat),str(lon),str(brg),str(vel))
                            print(localString)
#                           localString = gps.gpsread().strip.split(',')
                            sendUDP(leadCar[0], leadCar[1], "getLocation")  # a$
                            message = ["b'getLocation'",""] # prime the while loop
#                           message = s.recvfrom(BUFFER_SIZE) # message receive$
                            while(str(message[0])[2:-1] == "stop" or str(message[0])[2:-1] == "getLocation"):
#                           while(True):
                                #print("IN LOOP MESSAGE: ",message[0])
                                message = s.recvfrom(BUFFER_SIZE) # message received from guide car
                                #print("\n\nGUIDE CAR SENT:\n\t",message[0],"\n\n")
                                # if a stop signal is received stop the convoy
                                if(str(message[0])[2:-1] == "stop"):
                                    operate = False
                                    #sendUDP("<broadcast>",5555,"stop")
                                    break
                                elif(str(message[0])[2:-1] == "getLocation"):
                                    sendUDP(message[1][0], int(message[1][1]), str(localString))
                                else:
                                    guideString = str(message[0])[2:-1] # guideString obtained
                                    guideString = guideString.strip("\\n").split(',')
                                    localString = localString.strip("\\n").split(',')
                                    print(guideString)
                                    # calculate the offsets for the data and print them here
                                    # drive commands can be formed here as well
                                    print("\n-----------------------------------------------------------------")
                                    #print("Local PTP Data: " + str(localString))
                                    #print("Guide PTP Data: " + str(guideString))
                                    print("GPS DATA:")
                                    print("Guide Latitude: ", getLatitude(guideString))
                                    print("Local Latitude: ", getLatitude(localString))
                                    print("Guide Longitude: ", getLongitude(guideString))
                                    print("Local Longitude: ", getLongitude(localString))
                                    print("Guide Line of Bearing: ", getLineOfBearing(guideString))
                                    print("Local Line of Bearing: ", getLineOfBearing(localString))
                                    print("Guide Velocity: ", getVelocity(guideString))
                                    print("Local Velocity: ", getVelocity(localString))
                                    print("----------------------")
                                    speed = calculateSkid(guideString, localString, speed)
                                    #compare(guideString, localString)
                                    print("-------------------------------------------------------------------")
                                    if(operate == False):
                                        break;
                            time.sleep(0.5)   # add artificial delay so test dosnt run to fast to be boring
                            if(operate == False):
                                break;
                    #print("End of sample PTP data reached, process will now exit.")
                    fullStop()
                    break


                        # if a stop signal is received stop the convoy
#                        if(str(message[0])[2:-1] == "stop"):
#                            operate = False
#                            break
#                        guideString = str(message[0])[2:-1] # guideString o$
#                        guideString = guideString.strip("\\n").split(',')
#                        print("\n--------------------------------------------------------------------")
#                        print("Local PTP Data: " + str(localString))
#                        print("Guide PTP Data: " + str(guideString))
#                        print("Calculated Offsets:")
#                        speed = calculateSkid(guideString, localString, speed)
#                        #compare(guideString, localString)
#                        print("--------------------------------------------------------------------")
#                        speed = calculateSkid(guideString, localString, speed)


            # MOTOR SHUTOFF
            finally:
                fullStop()
                print("FULL STOP, CODE END")


main()
s.close()

