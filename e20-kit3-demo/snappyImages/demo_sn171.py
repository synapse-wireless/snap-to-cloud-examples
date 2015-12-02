# Copyright (C) 2014 Synapse Wireless, Inc.
"""Demo script for SN171 protoboard - status/control to E20 web interface"""

from nv_settings import *
from batmon import *

# I/O Pins
BUTTON = 20    # active low switch input
LED2_YLW = 5
LED1_GRN = 6

GRATUITOUS_STATUS_PERIOD = 5  # seconds

second_count = 0
button_count = 0

@setHook(HOOK_STARTUP)
def init():
    """Startup initialization"""
    # Set basic mesh parameters
    init_nv_settings(1, 1, True, True, False)
    
    # Init LEDs
    setPinDir(LED1_GRN, True)
    setPinDir(LED2_YLW, True)
    pulsePin(LED1_GRN, 500, True)
    pulsePin(LED2_YLW, 300, True)
    
    # Init switches
    setPinDir(BUTTON, False)
    setPinPullup(BUTTON, True)
    monitorPin(BUTTON, True)
    
@setHook(HOOK_1S)
def tick1sec():
    """Tick event handler"""
    global second_count
    second_count += 1
    if second_count == GRATUITOUS_STATUS_PERIOD:
        second_count = 0
        send_status()
    
@setHook(HOOK_GPIN)
def pin_event(pin, is_set):
    """Button press event handler"""
    global button_count
    if pin == BUTTON:
        if not is_set:
            button_count += 1
        send_status()

def send_status():
    """Broadcast a status RPC"""
    pulsePin(LED1_GRN, 50, True)
    mcastRpc(1, 3, 'status', batmon_mv(), not readPin(BUTTON), button_count)

def lights(pattern):
    """RPC call-in to set our LEDs to given pattern.
       For SN171 we just set LED2 on/off based on LSB of pattern
    """
    led_state = pattern & 1
    writePin(LED2_YLW, led_state)
