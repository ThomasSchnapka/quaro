import numpy as np


class SwingController:
    def __init__(self, state, touchdown_localizer):
        
        self.state = state
        self.touchdown_localizer = touchdown_localizer
        self.last_leg_state = np.array([1, 1, 1, 1]).astype(bool)
        
        
    def get_position(self, leg_state, leg_time):
        '''
        Args:
            leg_state: 1x4 bool with leg states. 1 = supporting, 0 = swinging
            leg_time: 1x4 array with normalized times [0, 1] for each leg
        Returns:
            3x4 np.array with normalized leg coordinates
                coordinates for non-swinging legs are 0
        To-Do:
            - Replace the beziere curve with some kind of curve that touches
              the middle point
            - implement 
            
        Info regarding normalized leg positions: the z-position is considered 1
        if all angles are zero (leg is fully streched out). z-position of the
        shoulder joint is 0, which means that the distance beween z=0 and z=1
        covers the full possible operating hight
        '''
        self.touchdown_localizer.update_touchdown_points(leg_state)
        p0 = self.touchdown_localizer.last_touchdown_point
        p2 = self.touchdown_localizer.next_touchdown_point
        
        # Calculate the middle point
        p1 = (p0 + p2)/2
        p1[2] *= self.state.swing_hight_factor
        
        pos = self.bezier(leg_time, p0, p1, p2)
        
        # remove positions of non-supporting legs
        pos *= ~leg_state 
        
        return pos
    
    
    def bezier(self, t, p0, p1, p2):
        '''
        Args:
            t: normailzed time in interval [0,1] for each leg, 1x4 np.array
            p0: starting point for bezier-curve for each leg,  3x4 np.array
            p1: middle point for bezier-curve for each leg,  3x4 np.array
            p2: end point for bezier-curve for each leg,  3x4 np.array
        Returns:
            coordinates on beziere shape for each leg 3x4 array
        '''
        b = (p0 - 2*p1 + p2)*t**2 + (-2*p0 + 2*p1)*t + p0
        return b
