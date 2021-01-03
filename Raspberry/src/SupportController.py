#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 22:30:26 2020

@author: Thomas
"""



class SupportController:
    def __init__(self, touchdown_localizer):
        
        self.touchdown_localizer = touchdown_localizer
        
        
    def get_position(self, leg_state, leg_time):
        '''
        Args:
            leg_state: 1x4 bool with leg states. 1 = supporting, 0 = swinging
            leg_time: 1x4 array with normalized times [0, 1] for each leg
        Returns:
            3x4 np.array with normalized leg coordinates
                coordinates for non-supporting legs are 0
                
        Info regarding normalized leg positions: the z-position is considered 1
        if all angles are zero (leg is fully streched out). z-position of the
        shoulder joint is 0, which means that the distance beween z=0 and z=1
        covers the full possible operating hight
        '''
        
        # addition with 0 to copy the array by values instead of whole object
        pos = self.touchdown_localizer.next_touchdown_point + 0 
        
        # alter only x and y axis
        pos[0:2] -= leg_time
        
        # remove positions of non-supporting legs
        pos *= leg_state 
        return pos
