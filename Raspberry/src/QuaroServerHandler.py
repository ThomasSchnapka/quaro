#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
In order to bind the server in it's own thread and not to block the user
interface, the QuaroServer object must be initialized outside of UserInterface,
which is done here

The reason for this rather uncovenient structure is the nature of pythons 
socket module which would block the UI without this solution
"""

from .QuaroServer import QuaroServer
import threading

class QuaroServerHandler:
    def __init__(self, state):
        self.state = state
        self.server_running = False
        self.quaro_server = None
        
    def start(self):
        '''creates server thread and starts it'''
        self.server_thread = threading.Thread(target=self.server_thread_control)
        self.server_thread.start()
        
    def server_thread_control(self):
        '''prepares parameters and starts server loop'''
        self.server_running = True
        self.state.allow_server_loop = True
        self.quaro_server = QuaroServer(self.state)
        if self.state.allow_server_loop == True:
            self.quaro_server.server_loop()
        
    def stop(self):
        '''stops server'''
        if self.server_running == True and self.state.allow_server_loop == True:
            self.state.allow_server_loop = False
            self.server_running = False
            print("[QuaroServerHandler] requested server to stop")
        


