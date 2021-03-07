import numpy as np
import time

class TransitionController:
    '''
    Controller for moving legs to new positions between states. E.g. if gait
    or mode is changed.
    '''
    
    def __init__(self, state, controller, hardware_config):
        self.state = state
        self.controller = controller
        self.hardware_config = hardware_config
        
        self.TOLERANCE = 0.2  # numeric tolerance for checking differences
        
    def current_time(self):
        '''return current system time in ms'''
        return int(round(time.time() * 1000))

    def leg_transition(self, new_pos, transition_time):
        '''
        Move legs from current position (saved in state) to new specified pos
        
        Messy because rather a choreography than tidy calculation.
        
        Basically, the algorith first aligns all z coordinates, that moves
        each single leg to it's new x/y-coordinate and set the new z
        coordinates in the last step
        
        Parameters
        ----------
        new_pos : (3x4) numpy.ndarray with target leg coordinates
        transition_time : in ms, maximal time for leg transition

        '''
        print("[TransitionController] moving legs to new position")
        old_pos = np.copy(self.state.uncorrected_foot_position)
        # check if any legs are still in air and set them on ground
        if np.any(np.abs(old_pos[2] - np.min(old_pos[2])) > self.TOLERANCE):
            t_align_z = transition_time*0.2
            transition_time -= t_align_z
            align_pos = np.copy(old_pos)
            align_pos[2] = np.max(old_pos[2])
            self.linear_transition(old_pos, align_pos, t_align_z)
            old_pos[2] = align_pos[2]
        # check if any legs have different x/y coordinates and change them
        if np.any(np.abs(old_pos[[0,1]] - new_pos[[0,1]]) > self.TOLERANCE):
            t_align_xy = transition_time*0.6
            transition_time -= t_align_xy
            # ensure same z
            align_pos = np.copy(new_pos)
            align_pos[2] = old_pos[2]
            # move legs seperately
            difference_in_xy = np.abs(align_pos[:2].sum(axis=0) - old_pos[:2].sum(axis=0))
            to_be_moved = np.argwhere(difference_in_xy > self.TOLERANCE)
            to_be_moved = to_be_moved[:, -1]
            amount = len(to_be_moved)
            target_pos = np.copy(old_pos)
            for n in to_be_moved:
                target_pos[:,n] = align_pos[:,n]
                self.quadratic_transition(old_pos, target_pos, t_align_xy/amount)
                old_pos = np.copy(target_pos)
        # check if legs are on requested z hight and change them
        if np.any(np.abs(old_pos[2] - new_pos[2]) > self.TOLERANCE):
            self.linear_transition(old_pos, new_pos, transition_time)
            
        
    def linear_transition(self, old_pos, new_pos, transition_time):
        '''move legs in beziere trajectory of order 1'''
        start_time = self.current_time()
        last_time = 0
        while (self.current_time() - start_time) < transition_time:
            if (self.current_time() - last_time) > self.state.update_time:
                t = (self.current_time() - start_time)/transition_time
                pos = (old_pos*(1-t) + new_pos*t)
                self.controller.set_leg_position(pos)
                last_time = self.current_time()
                
        
    def quadratic_transition(self, old_pos, new_pos, transition_time):
        '''move legs in beziere trajectory of order 2'''
        middle_pos = (old_pos + new_pos)/2
        middle_pos[2] *= 0.95 
        start_time = self.current_time()
        # save legs that remain on location in order to not move them
        remaining = np.all(old_pos == new_pos, axis=0)
        last_time = 0
        while (self.current_time() - start_time) < transition_time:
            if (self.current_time() - last_time) > self.state.update_time:
                t = (self.current_time() - start_time)/transition_time
                pos = (  (old_pos - 2*middle_pos + new_pos)*t**2 
                       + (-2*old_pos + 2*middle_pos)*t 
                       + old_pos)
                pos[:, remaining] = old_pos[:, remaining]
                self.controller.set_leg_position(pos)
                last_time = self.current_time()
                
    def raise_up(self, transition_time=3000):
        '''move robot from current to initial position'''
        print("[TransitionController] raising up")
        pos = np.zeros((3,4))
        pos[2] = (  self.state.operating_hight
                  *(self.hardware_config.l1 + self.hardware_config.l2))
        self.leg_transition(pos, transition_time)
        
    def lay_down(self, transition_time=3000):
        '''move robot from current to lay down position'''
        print("[TransitionController] laying down")
        pos = np.zeros((3,4))
        pos[2] = (  self.state.lay_down_hight
                  *(self.hardware_config.l1 + self.hardware_config.l2))
        self.leg_transition(pos, transition_time)
    
                
if __name__ == "__main__":
    # for testing the module
    class State:
        def __init__(self):
            self.update_time = 50
            self.absolute_foot_position = 0
            
    class Controller:
        def set_leg_position(self, arg):
            print(arg)
            
    state = State()
    controller = Controller()
    transition_controller = TransitionController(state, controller)
    
    state.absolute_foot_position = np.array([[ 0,  0,  0,  0],
                                             [ 0,  0,  0,  0],
                                             [20, 20, 10, 20]])
    new_pos = np.array([[ 0, 10, 10,  0],
                        [ 0,  0,  0,  0],
                        [20, 20, 20, 20]])
    transition_time = 1000
    transition_controller.leg_transition(new_pos, transition_time)                  
    