#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Contains data regarding robots current state
"""

import numpy as np
np.set_printoptions(precision=5)


class State:
    def __init__(self):
        
        self.support_ratio = 0.8
        self.phase = np.array([0.0, 0.25, 0.5, 0.75])
        
        self.cycle_time       = 3000.0
        self.update_time      = 10.0
        self.true_update_time = 0.0
        
        self.leg_state      = np.array([1, 1, 1, 1]).astype(bool)  # supporting or not
        self.last_leg_state = np.array([1, 1, 1, 1]).astype(bool)
        self.leg_time  = np.array([0, 0, 0, 0])
        self.velocity  = np.array([0.002, 0.0])    # x and y direction, in m/s
        self.roll     = 0.0
        self.pitch    = 0.0
        self.yaw      = 0.0
        self.z_stride = 0.0                        # maximal step height
        
        self.absolute_foot_position  = np.zeros((3, 4))
        self.normalized_foot_position  = np.zeros((3, 4))
        self.joint_angle    = np.zeros((3, 4))
        
        # start- and end-point of swing phase
        self.last_touchdown_point = np.array([[-0.5, -0.5, -0.5, -0.5],
                                              [-0.5, -0.5, -0.5, -0.5],
                                              [ 0.8,  0.8,  0.8,  0.8]])
        self.next_touchdown_point = np.array([[0.5, 0.5, 0.5, 0.5],
                                              [0.5, 0.5, 0.5, 0.5],
                                              [0.8, 0.8, 0.8, 0.8]])
        
    def debug(self):
        '''print all variables contained by this class, useful for debugging'''
        print "[State] debugging info"
        print "--------------------------------"
        variables = vars(self)
        for v in sorted(variables, key=len, reverse=True):
            print v, '\t', str(variables[v]).replace('\n', ' ')
        print "--------------------------------"
        

