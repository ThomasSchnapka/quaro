import numpy as np

class TouchdownLocalizer:
    '''Decides where to put leg time in next swing phase'''
    
    def __init__(self, state):
        
        self.state = state
        
        # start- and end-point of swing phase
        self.last_touchdown_point = np.copy(self.state.last_touchdown_point)
        
        self.next_touchdown_point = np.copy(self.state.next_touchdown_point)
        
    def update_touchdown_points(self, leg_state):
        '''
        check if leg changes from supporting to swing phase and update
        touchdown points if neccessary
        '''
        
        
        if self.state.leg_state is not self.state.last_leg_state:
            self.last_leg_state = self.state.leg_state
        
            first_time_swing = ~leg_state & ~(self.last_leg_state & leg_state)
        
            # set current location as old location
            self.last_touchdown_point.T[first_time_swing] = self.state.normalized_foot_position.T[first_time_swing]
        
            # TODO: implement better calculation of new touchdown-point
            self.next_touchdown_point.T[first_time_swing] = self.next_touchdown_point.T[first_time_swing]
            
            self.state.last_touchdown_point = self.last_touchdown_point
            self.state.next_touchdown_point = self.next_touchdown_point
            
            # verify values
            if (    np.any(self.state.next_touchdown_point > 1)
                and np.any(self.state.next_touchdown_point < 0)):
                # bad value encoutered
                self.state.debug()
                print "[controller] bad value in next_touchdown_point"
                print self.state.next_touchdown_point
                raise Exception("[TouchdownLocalizer] bad value encountered!")
            
            if (    np.any(self.state.last_touchdown_point > 1)
                and np.any(self.state.last_touchdown_point < 0)):
                # bad value encoutered
                self.state.debug()
                print "[controller] bad value in last_touchdown_point"
                print self.state.last_touchdown_point
                raise Exception("[TouchdownLocalizer] bad value encountered!")