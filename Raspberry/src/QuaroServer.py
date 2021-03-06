#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 10:29:54 2021

@author: Thomas
"""

import socket
import numpy as np


class QuaroServer:
    
    def __init__(self, state):
        # class params
        self.state = state
        self.allow_server_loop = True
        # server params
        self.IP = "192.168.2.111"
        self.IP_COMPUTER = "127.0.0.1"
        self.PORT = 1276
        self.TIMEOUT = 30
        self.HEADERSIZE = 10
        # setup server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            # when ran on Raspberry
            self.sock.bind((self.IP, self.PORT))
        except:
            # when ran on Computer
            self.IP = self.IP_COMPUTER
            self.sock.bind((self.IP, self.PORT))
        print("[QuaroServer] started server at", self.IP, self.PORT)
        self.sock.listen(1) # allow only one connection
        print(f"[QuaroServer] searching for sockets for max {self.TIMEOUT}s")
        self.sock.settimeout(self.TIMEOUT)
        try:
            self.clientsocket, self.address = self.sock.accept()
            print("[QuaroServer] sucessful connection with client!")
        except:
            print("[QuaroServer] timeout: no client available. Shutting down")
            self.state.allow_server_loop = False
            self.sock.close()
        
        
    
    def send(self, msg):
        '''
        Check msg-type, convert it to bytes, concatenate header and send it
        via socket
    
        Parameters
        ----------
        msg : numpy.ndarray (will be reconverted by socket) or arbitrary (will
              not be reconverted automaticly)
    
        '''
        if type(msg) == np.ndarray:
            content = msg.tobytes()
        else:
            content = bytes(msg)
        header = f"{len(content):<{self.HEADERSIZE}}"
        msg = bytes(header, 'utf-8') + content
        self.clientsocket.send(msg)

    def close(self):
        try:
            self.clientsocket.close()
            self.sock.close()
            self.state.allow_server_loop = False
            print("[QuaroServer] socket closed")
        except:
            #already closed
            pass
  
        
    def server_loop(self):
        # loop in which server runs until closed
        while self.state.allow_server_loop == True:
            cmd = self.clientsocket.recv(16)
            try:
                if cmd == b'abspos':
                    self.send(self.state.absolute_foot_position)
                elif cmd == b'norpos':
                    self.send(self.state.normalized_foot_position)
                elif cmd == b'joiang':
                    self.send(self.state.joint_angle)
                elif cmd == b'ropiya':
                    self.send(self.state.rpy)
                elif cmd == b'close':
                    print("[QuaroServer] close request from client side")
                    break
                elif cmd != b'':
                    print(f"[QuaroServer] data request {cmd} could not be resolved")
            except Exception as err:
                print("[QuaroServer] an error occured: ", err)
                break
        self.close()
        
#---------------------------- standalone test -------------------------------#

if __name__ == "__main__":
    print("[quaroServer] started standalone mode with dummy state class")
    class DummyState:
        def __init__(self):
            self.absolute_foot_position = np.zeros((3,4))
            self.allow_server_loop = True
    dummy_state = DummyState()
    qc = QuaroServer(dummy_state)
    qc.server_loop()


