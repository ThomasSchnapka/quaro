"""
Mostly taken from:
http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/
"""
import time


class PID:
    def __init__(self, kp, ki, kd, setpoint=0, f=None):
        '''
        TODO
        f is LP cutoff freq
        '''
        
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.err_sum = 0
        self.last_err = 0
        self.last_time = time.time()
        self.f = f
        self.last_value = 0
        
        
    def compute(self, current_value):
        # How long since we last calculated
        now = time.time()
        time_change = now - self.last_time
        
        # filter values if specified
        if self.f != None:
            # apply LP filter (Simple_infinite_impulse_response_filter)
            c = ((  2.0*3.1415*time_change*self.f     )
                  /(2.0*3.1415*time_change*self.f + 1 ))
            current_value = c*current_value + (1.0-c)*self.last_value
            self.last_value = current_value
            
        # Compute all the working error variables
        error = (self.setpoint - current_value)
        self.err_sum += (error * time_change)
        d_err = (error - self.last_err) / time_change
      
        # Compute PID Output
        output_value = (  self.kp * error
                        + self.ki * self.err_sum
                        + self.kd * d_err)
      
        # Remember some variables for next time
        self.last_err = error;
        self.last_time = now;
        
        return output_value
        
# TEST -----------------------------------------------------------------------

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    
    N = 100
    SETPOINT = 10
    pid = PID(1, 0.1, 1e-4, SETPOINT)
    
    x = np.zeros(N)
    
    for n in range(1, N):
        x[n] = x[n-1] + pid.compute(x[n-1])
        time.sleep(0.02)
        
    plt.plot(x)

