#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 21:42:21 2020

@author: Thomas
"""

import time
import numpy as np

class HardwareInterface:
    
    # inner class to be able to make tests without arduino connected
    class SerialDummy:
        def write(self, text):
            #print "Serial:", text
            return None
        def close(self):
            print "[serial] closed"
        def readline(self):
            return "<noDataAvailable>"
        
        
    def __init__(self, hardware_config):
        self.config = hardware_config
        self.serial = self.open_serial_connection()
        self.vals = np.empty(1) ###########################################################################
        
    def open_serial_connection(self):
        '''
        Try to open serial connection with Arduino
        If not possible, establish connection with serial dummy for testing
        returns serial handle
        '''
        serial = None
        for num in range(4):
            try:
                import serial
                serial = serial.Serial(port=('/dev/ttyUSB'+str(num)),
                                       baudrate = self.config.serial_baudrate,
                                       timeout = self.config.serial_timeout) 
                print "[serial] opened at " + self.serial.port
                time.sleep(1) # Arduino needs some time to establish connection
                break
            except:
                pass
        if serial is None:
            # serial connection could not be opened
            print ("[serial] could not open serial! " 
                   "Check ports with 'ls -l /dev/tty*'")
            serial = self.SerialDummy()
            print "[serial] established connection with serial dummy"
            
        return serial
    
        
    def send(self, data):
        self.serial.write("<" + data + ">")
        # print "[serial] sending: <" + data + ">"
        

    def receive(self):
        self.send('s') # request to send own data
        rec = self.serial.readline()
        while("<noDataAvailable>" not in rec):
            print "[serial] receiving: " + rec
            rec = self.serial.readline()  
            
        
    def send_angle(self, angle):
        angle = np.around(angle, 2)
        print "[HardwareInterface]", angle
        self.vals = np.append(self.vals, angle[0,0])
        #self.send(str(leg)+ ':a' + str(alpha) + 'b' + str(beta) + 'g' + str(gamma))
        #tell Arduino to send own data
        self.receive()
        
        
    def send_command(self, cmd):
        self.send(str(cmd))
        
    
    def shutdown(self):
        #Closes connection to serial, otherwise the port stays blocked
        self.serial.close()
        
    def plot(self):
        import matplotlib.pyplot as plt
        plt.plot(self.vals)