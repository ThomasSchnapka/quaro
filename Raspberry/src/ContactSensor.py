#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 13:42:26 2021

@author: Thomas
"""

import numpy as np
try:
    from smbus import SMBus
    addr = 0x8 # bus address
    bus = SMBus(1) # indicates /dev/ic2-1
except:
    print("[ContactSensor] could not connect to leg sensor")
    

class ContactSensor:
    
    def __init__(self):
        self.leg_state = np.zeros(4).astype(bool)
        pass
    
    def read(self):
        '''return contact sensor reading in 1x4 np bool array'''
        try:
            data = bus.read_byte_data(addr, 0)
            data = np.unpackbits(np.array(data, dtype=np.uint8),
                                 count=4,
                                 bitorder="little")
            self.leg_state = data.astype(bool)
        except:
            pass
        return self.leg_state
        