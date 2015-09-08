# Copyright (C) 2014 Synapse Wireless, Inc.
"""Demo script for SN173 protoboard - status/control to E20 web interface"""

from nv_settings import *
from batmon import *
from SN173 import *

GRATUITOUS_STATUS_PERIOD = 5  # seconds

second_count = 0
button_count = 0

BUTTON = S1

@setHook(HOOK_STARTUP)
def init():
    """Startup initialization"""
    # Set basic mesh parameters
    init_nv_settings(1, 1, True, True, False)
    
    # Init LEDs
    setPinDir(LED1, True)
    setPinDir(LED2, True)
    setPinDir(LED3, True)
    setPinDir(LED4, True)
    pulsePin(LED1, 500, True)
    pulsePin(LED2, 300, True)
    pulsePin(LED3, 200, True)
    pulsePin(LED4, 100, True)
    
    # Init switches
    for s in SWITCH_TUPLE:
        setPinDir(s, False)
        setPinPullup(s, True)
        monitorPin(s, True)
    
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
    pulsePin(LED4, 50, True)
    mcastRpc(1, 3, 'status', batmon_mv(), not readPin(BUTTON), button_count)

def lights(pattern):
    """RPC call-in to set our LEDs to given pattern.
       For SN173 we'll set 2 LEDs, but we could get a little fancier in the future.
    """
    led_state = pattern & 1
    writePin(LED1, led_state)
    writePin(LED2, led_state)
