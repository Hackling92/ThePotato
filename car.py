import socket
import threading

BUFFER_SIZE = 1500
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


def main():

    localString = "localString here"

    global startPressed

    id = int(input("Vehicle ID Number: "))


    if(id == 1):
        print("Leader")
        s.bind(("", 5555))
        isSetup = False
        while(not isSetup):
            message = s.recvfrom(BUFFER_SIZE)
            if(clientInList(message[1])):
                # check to see if message is start
                if(str(message[0])[2:-1] == "start"): # a vehicle requested to start run
                    isSetup = True
                    sendHeadToClient()
            else:
                clients.append(message[1])
            print(clients)

        while(True):
            #put any processing data here


            message = s.recvfrom(BUFFER_SIZE) # get location request
            if(str(message[0])[2:-1] == "getLocation"):
                sendUDP(message[1][0],message[1][1], localString)


    else:
        print("Follower Number", (id - 1))
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sendUDP("<broadcast>",5555,"client" + str(id))
        while(True):
            if(startPressed):
                sendUDP("<broadcast>", 5555, "start")
                recData = s.recvfrom(BUFFER_SIZE) # get your leader and save it
                leadAdd, leadPort = str(recData[0])[2:-1].split(':')
                leadCar = (leadAdd, int(leadPort))
                print(leadCar)
                break
            startPressed = int(input("Start: "))
            # need parallel code here to check if packet start came in
        while(True):
            sendUDP(leadCar[0],leadCar[1],"getLocation") # ask for location from lead car
            message = s.recvfrom(BUFFER_SIZE)
            guideString = str(message[0])[2:-1]

            # do comparison here




main()
s.close()