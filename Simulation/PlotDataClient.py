#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client for Quaro Server

Intended for use as datasource for the QuaroPlot3D module

Client will search for server for 30 seconds and shut down afterwards
"""

import socket
import numpy as np
import time


class PlotDataClient:
    
    def __init__(self):
        # setup socket
        self.HEADERSIZE = 10
        self.IP = "192.168.2.111"
        self.PORT = 1276
        
        for attempt in range(1, 5+1):
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.s.connect((self.IP, self.PORT)) # server binds, sockets connect
                print("[PlotDataClient] sucessful connection!")
                break
            except:
                print("[PlotDataClient] connection not possible, "\
                      f"will try again in five seconds (attempt: {attempt}/5)")
                time.sleep(5)
                if attempt == 5:
                    raise Exception("[PlotDataClient] connection failed. "\
                                    "Is the server running?") 
        
          
    def receive(self):
        '''
        receive message from socket
    
        Returns
        -------
        received unformated bytes
    
        '''
        full_msg = b'' #empty byte array
        new_msg = True
        while True:
            msg = self.s.recv(16)
            if new_msg and msg != b'':
                msglen = int(msg[:self.HEADERSIZE])
                new_msg = False
            full_msg += msg
            if len(full_msg)-self.HEADERSIZE >= msglen:
                # remove header
                full_msg = full_msg[self.HEADERSIZE:]
                return full_msg
           
    def convert_msg(self, msg, msg_type, size=(3,4)):
        '''
        Convert received messages from bytes to stated type
    
        Parameters
        ----------
        msg: received message (byte array)
        msg_type: type the messages shall be converted to
        size: if type=np.ndarray, array shape
              optional, the default is (3,4).
    
        Returns
        -------
        converted message of type msg_type
    
        '''
        if msg_type == np.ndarray:
            return np.frombuffer(msg).reshape(size)
        else:
            return str(msg)
                
    def request_data(self, req_data):
        '''
        request certain data from client
        
        Parameters
        ----------
        req_data: string, possible datatypes:
                  abspos: (3,4) np.ndarray with absolute foot positions
                  norpos: (3,4) np.ndarray with normalized foot positions
                  joiang: (3,4) np.ndarray with leg angles
                  ropija: (1,3) np.ndarray with roll, pitch, yaw
                   
        Returns
        ---------
        requested data in appropriate form
        '''
        if req_data in ["abspos", "norpos", "joiang"]:
            self.s.send(bytes(req_data, 'utf-8'))
            msg = self.receive()
            return self.convert_msg(msg, np.ndarray)
        if req_data in ["ropiya"]:
            self.s.send(bytes(req_data, 'utf-8'))
            msg = self.receive()
            return self.convert_msg(msg, np.ndarray, 3)
        else:
            return "Request not understood"
        
    
    def close(self):
        # ask server to close and close client socket
        print("[PlotDataClient] requested server to close")
        self.s.send(b"close")   # tell server to close
        self.s.close()
        
