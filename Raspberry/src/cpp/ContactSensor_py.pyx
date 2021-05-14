#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Makes ContactSensor.py available to C++
"""

try:
    from smbus import SMBus
    addr = 0x8 # bus address
    bus = SMBus(1) # indicates /dev/ic2-1
except:
    print("[ContactSensor] could not connect to leg sensor")
    
# force cython to generate header
cdef public int i
    
cdef public int read_bytes():
    '''similar to above function, but sends bytes instead of array'''
    cdef int data
    try:
        data = bus.read_byte_data(addr, 0)
    except:
        data = bytes("8")
    return data
        
    

