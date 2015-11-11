# Copyright (C) 2015 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse") to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR) ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS DISCLAIMER.

"""
This example script only toggles the stat of the LEDs when a button is pushed or an RPC is received
to toggle the LED.

This example script is meant to work with an example program on the E20 for demonstrating the use
of Tornado using the iploop as the scheduler for the system.

This script is independant of that program as this script only reports status and done not
require polling from the gateway for the buttons to toggle the state of the LEDs.
"""

from synapse.platforms import *
#from synapse.SM220 import *

# Define variables that can be used easily and be meaningful in the script space blow.
# Allows one place to change all the parameters if needed.
LED1 = GPIO_D2
LED2 = GPIO_D1
LED3 = GPIO_B2
LED4 = GPIO_F4
BUTTON1 = GPIO_C3
BUTTON2 = GPIO_F1
BUTTON3 = GPIO_F2
BUTTON4 = GPIO_F3


# Define constants (variables that are not intended to change at run time.
HOP_COUNT = 4

# Define inital state of global variables
StatusUpdateCount = 1  # set to one so that on the first time through the 1 second hook it will update.

 #This means to use the function below as a callback on startup.
@setHook(HOOK_STARTUP)
def startupEvent():    
    """run automatically after unit startup or download"""
    
    # write the initial state of the pin that we desire and then set them to be outputs
    writePin(LED1, False)
    writePin(LED2, False)
    writePin(LED3, False)
    writePin(LED4, False)
    setPinDir(LED1, True)
    setPinDir(LED2, True)
    setPinDir(LED3, True)
    setPinDir(LED4, True)
    
    # Set up our button pins to be inputs
    setPinDir(BUTTON1, False)
    setPinDir(BUTTON2, False)
    setPinDir(BUTTON3, False)
    setPinDir(BUTTON4, False)
    
    # Enable the internal pull ups on the button pins so we can monitor 
    # the change in status when the button pulls the pin voltage low.
    setPinPullup(BUTTON1, True)
    setPinPullup(BUTTON2, True)
    setPinPullup(BUTTON3, True)
    setPinPullup(BUTTON4, True)
    
    # Monitor for button-press events
    monitorPin(BUTTON1, True)
    monitorPin(BUTTON2, True)
    monitorPin(BUTTON3, True)
    monitorPin(BUTTON4, True)
    
def clearAllLEDs():
    """Clear all LEDs or turn them all off on the SN-173"""
    writePin(LED1, False)
    writePin(LED2, False)
    writePin(LED3, False)
    writePin(LED4, False)

def reportStateAllLEDs():
    """Command that will cause the allLedState method to be sent with the status of all 4 user LEDs"""
    # Read the status of the pin for each LED drive
    led1State = readPin(LED1)   
    led2State = readPin(LED2)
    led3State = readPin(LED3)
    led4State = readPin(LED4)
    # Generate an mcast output to anyone who processes this message.
    mcastRpc(1, HOP_COUNT, 'updateLEDs', led1State, led2State, led3State, led4State)
    
def buttonS1pressed():
    """Toggle the state of LED1 and send an mcast message about the ledState"""
    var = readPin(LED1)
    var = not var
    writePin(LED1, var)
    reportStateAllLEDs()
    
def buttonS2pressed():
    """Toggle the state of LED2 and send an mcast message about the ledState"""
    var = readPin(LED2)
    var = not var
    writePin(LED2, var)
    reportStateAllLEDs()

def buttonS3pressed():
    """Toggle the state of LED3 and send an mcast message about the ledState"""
    var = readPin(LED3)
    var = not var
    writePin(LED3, var)
    reportStateAllLEDs()

def buttonS4pressed():
    """Toggle the state of LED4 and send an mcast message about the ledState"""
    var = readPin(LED4)
    var = not var
    writePin(LED4, var)
    reportStateAllLEDs()
    
def reset_pressed():
    reboot()

@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    """Hooked into the HOOK_GPIN event"""

    # Test each pin that we are monitoring to see if that was the one triggering the event.
    # Test if the isSet is False indicating the button is pressed down, we only want to toggle
    # the LED on a press, not a release of the button.
    if pinNum == BUTTON1:
        if isSet == False:
            buttonS1pressed()
    elif pinNum == BUTTON2:
        if isSet == False:
            buttonS2pressed()
    elif pinNum == BUTTON3:
        if isSet == False:        
            buttonS3pressed()
    elif pinNum == BUTTON4:
        if isSet == False:
            buttonS4pressed()

@setHook(HOOK_1S)
def oneSecondHook():
    """Hooked into the one second tick to perform this function each second"""
    global StatusUpdateCount
    
    mcastRpc(1, HOP_COUNT, 'powerOn173', True)
    
    # Have the node periodically send an update of its status, set for 10 seconds
    StatusUpdateCount -= 1
    if StatusUpdateCount <= 0:
        reportStateAllLEDs()
        StatusUpdateCount = 10
    
    
    