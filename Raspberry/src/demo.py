#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 13:28:55 2021

@author: Thomas
"""

import numpy as np
import time



def start_demo(controller, demo_type="rpy"):
    '''initated demo depending on demanded demo type'''
    if demo_type == "rpy":
        do_rpy_demo(controller)
    elif demo_type == "pushups":
        do_pushups(controller)
    elif demo_type == "twerk":
        do_twerk(controller)

def get_initial_position():
    '''leg position the demo starts with, used for transition'''
    coordinates = np.zeros((3,4))
    coordinates[0] = 0
    coordinates[2] = 220
    return coordinates

def do_rpy_demo(controller):
    '''changes roll, pitch and yaw'''
    # parameters
    UPDATE_TIME = 30
    RPY_AMOUNT = 2
    RPY_TIME = 8000     # ms, total time per iteration
    # amplitudes
    ROLL = 15            # degree
    PITCH = 5           # degree
    YAW = 15             # degree
    
    # calculation
    coordinates = get_initial_position()
    start_time = current_time()
    last_time = 0
    print("[Demo] starting demo: RPY demonstration")
    for n in range(RPY_AMOUNT):
        # roll
        print("[Demo] roll")
        start_time = current_time()
        while (current_time() - start_time) < RPY_TIME/3:
            if (current_time() - last_time) > UPDATE_TIME:
                t = (current_time() - start_time)/(RPY_TIME/3)
                angle = ROLL*np.sin(2*np.pi*t)
                controller.set_leg_position(coordinates, np.array([angle, 0, 0]))
                last_time = current_time()
        # pitch
        print("[Demo] pitch")
        start_time = current_time()
        while (current_time() - start_time) < RPY_TIME/3:
            if (current_time() - last_time) > UPDATE_TIME:
                t = (current_time() - start_time)/(RPY_TIME/3)
                angle = PITCH*np.sin(2*np.pi*t)
                controller.set_leg_position(coordinates, np.array([0, angle, 0]))
                last_time = current_time()
        # yaw
        print("[Demo] yaw")
        start_time = current_time()
        while (current_time() - start_time) < RPY_TIME/3:
            if (current_time() - last_time) > UPDATE_TIME:
                t = (current_time() - start_time)/(RPY_TIME/3)
                angle = YAW*np.sin(2*np.pi*t)
                controller.set_leg_position(coordinates, np.array([0, 0, angle]))
                last_time = current_time()
                
       
                
def do_twerk(controller):
    ''' rapidly move the back up and down to arouse other robots interest'''
    # parameters
    UPDATE_TIME = 30
    TWERK_AMOUNT = 10
    TWERK_TIME = 800     # ms, total time per iteration
    # amplitudes
    MAX_ANGLE = 3
    CENTER_OF_ROTATION = np.array([-186/2, 0, 0])
    
    # calculation
    coordinates = np.zeros((3,4))
    coordinates[2] = 220
    start_time = current_time()
    last_time = 0
    print("[Demo] twerking: rapidly move the back up and down to arouse "\
          "other robots interest")
    for n in range(TWERK_AMOUNT):
        # pitch
        start_time = current_time()
        while (current_time() - start_time) < TWERK_TIME:
            if (current_time() - last_time) > UPDATE_TIME:
                t = (current_time() - start_time)/(TWERK_TIME)
                angle = MAX_ANGLE*np.sin(2*np.pi*t)
                controller.set_leg_position(coordinates,
                                            np.array([0, angle, 0]),
                                            CENTER_OF_ROTATION)
                last_time = current_time()
    
    
    
def do_pushups(controller):
    # parameters
    UPDATE_TIME = 30
    PUSHUP_AMOUNT = 5
    PUSHUP_TIME = 3000.0
    
    # calculation
    start_time = current_time()
    last_time = 0
    print("[Demo] starting demo: pushups")
    for n in range(PUSHUP_AMOUNT):
        print("[Demo] Pushup Nr.", n+1)
        start_time = current_time()
        while (current_time() - start_time) < PUSHUP_TIME:
            if (current_time() - last_time) > UPDATE_TIME:
                t = (current_time() - start_time)/PUSHUP_TIME
                angle = pushups(t)
                controller.set_leg_angle(angle)
                last_time = current_time()
    
def pushups(t):
    angle = np.zeros((3,4))
    angle[0] =  15*np.sin(2*np.pi*t)
    angle[1] = -30*np.sin(2*np.pi*t)
    angle[:,[1,2]] *= -1
    return angle
    
    
def current_time():
    '''return current system time in ms'''
    return int(round(time.time() * 1000))

    