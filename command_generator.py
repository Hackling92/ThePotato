#######################################################
# Team:         CCP2 (The Potato)
# Email:        candre1@umbc.edu
#               cu61692@umbc.edu
#               hash4@umbc.edu
#               wj1@umbc.edu
# File:         command_generator.py
# Description:  This file will be used to generate
#               vehicle commands to be sent to the
#               iRobot vehicles.
#######################################################

# INCLUDE
import math
from motor_control import *
from packet_parser import *

#######################################################
## CALCULATION FUNCTIONS
#######################################################

## calculateDir #######################################
# Inputs:       guideString, localString
# Outputs:      "Forward" or "Reverse"
# Description:  This function determines what direction
#               the vehicle should proceed. Determined
#               by listed inputs.
#######################################################
def calculateDir(guideString, localString):
    # If local velocity == 0 and distance is decreasing
    # then reverse
    if (getVelocityX(localString) >= 0) and (getVelocityX(guideString) <= 0):
        dir = "Reverse"
    elif (getVelocityX(localString) <= 0) and (getVelocityX(guideString) >= 0):
        dir = "Reverse"
    # else, Forward
    else:
        dir = "Forward"
    return dir

## calculateRadius ####################################
# Inputs:       guideString, localString
# Outputs:      Radius in meters
# Description:  This function determines what radius
#               the vehicle will turn around. This is
#               Determined by listed inputs.
#######################################################
def calculateRadius(guideString, localString):
    # HOW-TO
    # - use calculated distance.
    #   - distance = sqrt(deltaLat**2 + deltaLong**2)
    # - angle (theta) is angle between localBearing and
    #   vector to the guide vehicle.
    #   - theta = vectorAngle - localBearing
    #   - vectorAngle = tan-1(long/lat) !! USE THIS TO CALCULATE BEARING
    # - then radius = distance * cos(90 - theta).
    deltaLong = getLongitude(guideString) - getLongitude(localString)
    deltaLat = getLatitude(guideString) - getLatitude(localString)
    distance = math.sqrt(deltaLong**2 + deltaLat**2)
    bearing = getLineOfBearing(localString)
    vectorAngle = math.atan2(deltaLong, deltaLat)
    theta = vectorAngle - localBearing
    radius = distance * math.cos(((math.pi)/2) - theta)
    #radius = 4
    return radius

## calculateSpeed #####################################
# Inputs:       guideString, localString
# Outputs:      Speed factor (0-100)
# Description:  This function determines the speed
#               the vehicle should drive at. Determined
#               by listed inputs.
#######################################################
def calculateSpeed(guideString, localString, currentSpeed):
    # Velocity difference between vehicles
    guideSquareX = getVelocityX(guideString)**2
    guideSquareY = getVelocityY(guideString)**2
    localSquareX = getVelocityX(localString)**2
    localSquareY = getVelocityY(localString)**2
    guideVelocity = math.sqrt(guideSquareX + guideSquareY)
    localVelocity = math.sqrt(localSquareX + localSquareY)
    # Same velocities
    if (guideVelocity == localVelocity):
        newSpeed = currentSpeed
    # Guide faster than local
    elif (guideVelocity > localVelocity):
        newSpeed = currentSpeed + 5
    # Local faster than guide
    elif (guideVelocity < localVelocity):
        newSpeed = currentSpeed - 5
    return newSpeed

## calculateBearing ###################################
# Inputs:       guideString, localString
# Outputs:      Bearing as angle in degrees (0-360)
# Description:  This function determines what direction
#               the guide vehicle is in relation to the
#               local vehicle.
#######################################################
def calculateBearing(guideString, localString):
    # see CalculateRadius
    deltaLong = getLongitude(guideString) - getLongitude(localString)
    deltaLat = getLatitude(guideString) - getLatitude(localString)
    bearing = math.atan2(deltaLong, deltaLat)
    #bearing = 20
    return bearing

## calculateSkid ######################################
# Inputs:       guideString, localString
# Outputs:      None, executes skidSteer command
# Description:  This function will use the location
#               data to generate the values needed
#               to perform vehicle movements.
#######################################################
def calculateSkid(guideString, localString, speed):
    # Do calculations
    dir = calculateDir(guideString, localString)
    radius = calculateRadius(guideString, localString)
    newSpeed = calculateSpeed(guideString, localString, speed)
    bearing = calculateBearing(guideString, localString)
    # Execute skid steer
    #skidSteer(dir, radius, newSpeed, bearing)
    # Return speed for future calculations
    print("----------------------")
    print ("VALUES FOR SKIDSTEER:")
    print ("dir =      ", dir)
    print ("radius =   ", radius)
    print ("newSpeed = ", newSpeed)
    print ("bearing =  ", bearing)
    print ("---------------------")
    return newSpeed




#######################################################
## COMPARE FUNCTIONS
#######################################################

## compareAvePtpFlag ##################################
# Inputs:       guideAvePtpFlag, localAvePtpFlag
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareAvePtpFlag(guideAvePtpFlag, localAvePtpFlag):
    # Check guideAvePtpFlag
    if(guideAvePtpFlag == "true"):
        print("  Following AVE Unit")
    else:
        print("  Following iRobot Unit")
    # Check localAvePtpFlag
    if(localAvePtpFlag == "true"):
        print("  I am an AVE Unit")
    else:
        print("  I am an iRobot Unit")
    return 0

## compareLeaderFollowerFlag ##########################
# Inputs:       guideLeaderFollowerFlag, localLeaderFollowerFlag
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareLeaderFollowerFlag(guideLeaderFollowerFlag, localLeaderFollowerFlag):
    # Check guideLeaderFollowerFlag
    if(guideLeaderFollowerFlag == "true"):
        print("  Following Convoy Leader")
    else:
        print("  Following Secondary Convoy Unit")
    # Check localLeaderFollowerFlag
    if(localLeaderFollowerFlag == "true"):
        print("  I am the Convoy Leader")
    else:
        print("  I am a Secondary Convoy Unit")
    return 0

## comparePositionInConvoy ############################
# Inputs:       guidePositionInConvoy, localPositionInConvoy
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def comparePositionInConvoy(guidePositionInConvoy, localPositionInConvoy):
    print("  Guide UID: " + guidePositionInConvoy)
    print("  Local UID: " + localPositionInConvoy)
    return 0

## compareEmergencyStop ###############################
# Inputs:       guideEmergencyStop, localEmergencyStop
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareEmergencyStop(guideEmergencyStop, localEmergencyStop):
    if((guideEmergencyStop == "true") or (localEmergencyStop == "true")):
        print("  Emergency Stop Detected")
        fullStop()        # MOTOR SHUTOFF
    else:
        print("  System Status OK")
    return 0

## compareLatitude ####################################
# Inputs:       guideLatitude, localLatitude
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareLatitude(guideLatitude, localLatitude):
    if(float(guideLatitude) != float(localLatitude)):
        print("  Different Latitude, Adjust Position")
        #runspeed = 10
        #reverse(runspeed)        # FOR TESTING
    else:
        print("  Same Latitude")
    return 0

## compareLongitude ###################################
# Inputs:       guideLongitude, localLongitude
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareLongitude(guideLongitude, localLongitude):
    if(float(guideLongitude) != float(localLongitude)):
        print("  Different Longitude, Adjust Position")
        #runspeed = 10
        #forward(runspeed)        # FOR TESTING
    else:
        print("  Same Longitude")
    return 0

## compareLineOfBearing ################################
# Inputs:       guideLineOfBearing, localLineOfBearing
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareLineOfBearing(guideLineOfBearing, localLineOfBearing):
    if(float(guideLineOfBearing) != float(localLineOfBearing)):
        print("  Different Line of Bearing, Turn Vehicle")
    else:
        print("  Same Line of Bearing")
    return 0

## compareVelocityX ###################################
# Inputs:       guideVelocityX, localVelocityX
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareVelocityX(guideVelocityX, localVelocityX):
    if(float(guideVelocityX) > float(localVelocityX)):
        print("  Slower VelocityX, Speed Up")
    elif(float(guideVelocityX) < float(localVelocityX)):
        print("  Faster VelocityX, Slow Down")
    else:
        print("  Same VelocityX, Maintain Speed")
    return 0

## compareVelocityY ##################################
# Inputs:       guideVelocityY, localVelocityY
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareVelocityY(guideVelocityY, localVelocityY):
    if(float(guideVelocityY) > float(localVelocityY)):
        print("  Slower VelocityY, Speed Up")
    elif(float(guideVelocityY) < float(localVelocityY)):
        print("  Faster VelocityY, Slow Down")
    else:
        print("  Same VelocityY, Maintain Speed")
    return 0

## compareVelocityZ ###################################
# Inputs:       guideVelocityZ, localVelocityZ
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareVelocityZ(guideVelocityZ, localVelocityZ):
    if(float(guideVelocityZ) > float(localVelocityZ)):
        print("  Slower VelocityZ, Speed Up")
    elif(float(guideVelocityZ) < float(localVelocityZ)):
        print("  Faster VelocityZ, Slow Down")
    else:
        print("  Same VelocityZ, Maintain Speed")
    return 0

## compareAccelerationX ###############################
# Inputs:       guideAccelerationX, localAccelerationX
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareAccelerationX(guideAccelerationX, localAccelerationX):
    if(float(guideAccelerationX) > float(localAccelerationX)):
        print("  Slower AccelerationX, Speed Up")
    elif(float(guideAccelerationX) < float(localAccelerationX)):
        print("  Faster AccelerationX, Slow Down")
    else:
        print("  Same AccelerationX, Maintain Speed")
    return 0

## compareAccelerationY ###############################
# Inputs:       guideAccelerationY, localAccelerationY)
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareAccelerationY(guideAccelerationY, localAccelerationY):
    if(float(guideAccelerationY) > float(localAccelerationY)):
        print("  Slower AccelerationY, Speed Up")
    elif(float(guideAccelerationY) < float(localAccelerationY)):
        print("  Faster AccelerationY, Slow Down")
    else:
        print("  Same AccelerationY, Maintain Speed")
    return 0

## compareAccelerationZ ###############################
# Inputs:       guideAccelerationZ, localAccelerationZ
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareAccelerationZ(guideAccelerationZ, localAccelerationZ):
    if(float(guideAccelerationZ) > float(localAccelerationZ)):
        print("  Slower AccelerationZ, Speed Up")
    elif(float(guideAccelerationZ) < float(localAccelerationZ)):
        print("  Faster AccelerationZ, Slow Down")
    else:
        print("  Same AccelerationZ, Maintain Speed")
    return 0

## compareExtraData ###################################
# Inputs:       guideExtraData, localExtraData
# Outputs:      N/A
# Description:  
#               
#               
#######################################################
def compareExtraData(guideExtraData, localExtraData):
    return 0
