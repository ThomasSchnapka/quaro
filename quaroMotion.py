__version__ = '1'
__author__ = 'Thomas Schnapka'

import time
import numpy as np
import quaroShared as sh


gait_active = False #stops Gait if necessary

cur_time = lambda: int(round(time.time() * 1000))

sh.Data.last_cycle_time = cur_time() #must be set during setup

#angles
f = np.array([0.0, 0.0, 0.0, 0.0])
t = np.array([0.0, 0.0, 0.0, 0.0])
c = np.array([0.0, 0.0, 0.0, 0.0])


def get_angles(inp_x, inp_y, inp_z):
    '''
    Returns all joint angles to a given set of coordinates considering the 
    robots geometry and the current position of COM.
    
    Args:
        inp_x, inp_y, inp_z: Numpy-Array with coordinates for every leg
        
    Returns:
        f, t, c:  Numpy-Array with angles for every joint
    '''
    x = inp_x + 0.0
    y = inp_y + 0.0
    z = inp_z + 0.0
    
    def calc_angles(x, y, z):
        f_angle = np.array([0.0, 0.0, 0.0, 0.0])
        t_angle = np.array([0.0, 0.0, 0.0, 0.0])
        c_angle = np.array([0.0, 0.0, 0.0, 0.0])
        try:
            h1 = np.sqrt(y**2 + (sh.Data.hight+z)**2)
            h2 = np.sqrt(x**2 + y**2 + (sh.Data.hight+z)**2)
            f_angle = ((np.arctan(x/h1) + np.arccos(h2 / (2.0*sh.Data.leglen))) 
                        * (360.0/(2.0*np.pi)))
            t_angle = (2.0 * np.arccos(h2 / (2.0*sh.Data.leglen))
                        * (360.0 / (2.0*np.pi)))
            c_angle = np.arcsin(y / (sh.Data.hight+z)) * (360.0/(2.0*np.pi))
        except:
            sh.Data.gait_active = False
            print "[Error]\nCould not calculate angles, bad coordinates!"
            print "x:", x, "\ny:", y, "\nz:", z, "\n"
        return f_angle, t_angle, c_angle
    
    def calc_com(f, t, c):
        '''
        Calculates the "real" COM considering the bodys mass as well as
        the joints current position and their mass
        '''
        cc_f = f * (2.0*np.pi/360.0)
        cc_t = t * (2.0*np.pi/360.0)
        cc_c = c * (2.0*np.pi/360.0)
        calc_com = sh.Data.com * 1.0
        for i in range(4):
            calc_com[0] +=  ((((sh.Data.leglen-sh.Data.com_leg)
                                * np.sin(cc_t[i]-cc_f[i])) 
                                - (sh.Data.leglen*np.sin(cc_f[i]))) 
                                * sh.Data.mass_motor)
            calc_com[2] += ((sh.Data.leglen*np.cos(cc_f[i]) 
                            - (sh.Data.leglen-sh.Data.com_leg)
                            * np.sin(cc_t[i]-cc_f[i])) * sh.Data.mass_motor)
            calc_com[1] += ((np.sqrt(calc_com[0]**2 + calc_com[2]**2)
                            * np.sin(cc_c[i])) * sh.Data.mass_motor)
        for i in range(3):
            calc_com[i] += sh.Data.com_body[i] * sh.Data.mass_body
            calc_com[i] /= sh.Data.mass_body + (4.0*sh.Data.mass_motor)
        calc_com[0] += sh.Data.com_adjust[0]
        calc_com[1] += sh.Data.com_adjust[1]
        if sh.Data.simulation_active:
            sh.send_data(('j', calc_com[0])) #x
            sh.send_data(('k', calc_com[1])) #y
            sh.send_data(('l', calc_com[2])) #z
        return calc_com
    
    if sh.Data.calc_com_active:
        f, t, c = calc_angles(x, y, z)
        calc_com = calc_com(f, t, c)
        x -= calc_com[0]
        y -= calc_com[1]
        
    f, t, c = calc_angles(x, y, z)
    return f, t, c


def balance(x, y, z):
    '''
    Shifts the COM into the support triangle for non-periodic movements such as
    demo(). For gaits, dodge() is used.
    
    Args:
        x, y, z: Numpy-Arrays with coordinates for every leg
        
    Returns:
        x, y, z: Recalculated coordinates for every leg
    '''
    
    num = 0
    legs = np.array([])
    del_x = 0.0
    del_y = 0.0
    #check which feet are not supporting:
    for n in range(4):
        if z[n] < 0:
            num += 1
            legs = np.append(legs, n)
    if num is 1:   #if only one leg raised:
        length = sh.Data.amplitude_balance*np.sqrt(x[int(legs[0])]**2
                + y[int(legs[0])]**2 + z[int(legs[0])]**2)
        del_x = length*np.cos(sh.Data.teta_0[num])
        del_y = length*np.sin(sh.Data.teta_0[num])
    for n in range(4): #only change the supporting feet 
        if n not in legs:
            x[n] -= del_x
            y[n] -= del_y
    return x,y,z


def beziere(cur_time, p0=np.array([0.0,0.0,0.0]), p2=np.array([0.0,0.0,0.0]),
            p1=np.array([0.0,0.0,-0.65*sh.Data.hight]),
            duration = 1.0-sh.Data.support_ratio):
    '''
    Returns leg-coordinates for a Beziere-Curve-shaped trajectory. 
    Args:
        cur_time: current cycle_time, between 0 and duration
        p0: starting-coordinates of trajectory
        p1: end-coordinates of trajectory
        p1: vertex of trajectory
        duration: how long the movement takes to get from p0 to p1
    Returns:
        p_beziere: Numpy-Array with single-leg-coordinates [x,y,z]
    '''
    bez_time = cur_time/duration
    p_beziere = np.array([0.0, 0.0, 0.0])
    for i in range(3):
        p_beziere[i] = ((p0[i]-2.0*p1[i]+p2[i])*(bez_time**2)
                        + (-2.0*p0[i]+2.0*p1[i])*bez_time + p0[i])
    return p_beziere #corresponds to [x,y,z]


def gait_loop():
    '''
    Loop that controles the gait, to be called in a own thread.
    '''
    def dodge(ct):
        '''
        Returns the distance the oscillating COM gets shifted for every frame. 
        Used for periodic movements, for static ones balance()
        
        Args:
            ct: current cycleTime between 0 and 1
        
        Returns:
            dodge_x, dodge_y: amount of shifting of COM per direction
        '''
        dodge_x = 0.0
        dodge_y = 0.0
        dodge_dist = np.array([0.0, 0.0, 0.0, 0.0])
        for i in range(4):
            if ct[i] <= sh.Data.dodge_time:
                dodge_dist[i] = (sh.Data.amplitude_dodge
                                * (1 - (ct[i]/sh.Data.dodge_time)))
            elif ct[i] <= sh.Data.support_ratio-sh.Data.dodge_time:
                dodge_dist[i] = 0
            elif ct[i] <= sh.Data.support_ratio:
                dodge_dist[i] = (sh.Data.amplitude_dodge
                                * ((ct[i] - (sh.Data.support_ratio
                                -sh.Data.dodge_time)) / (sh.Data.dodge_time)))
            else:
                dodge_dist[i] = sh.Data.amplitude_dodge
            dodge_x += -(1.0) * dodge_dist[i] * np.sin(sh.Data.teta_0[i])
            dodge_y += (1.0) * dodge_dist[i] * np.cos(sh.Data.teta_0[i])
        return dodge_x, dodge_y
    
    def crt(i, ct=0.0):
        '''
        COM-relative-trajectory
        
        Args:
            i: leg number
            ct: current cycleTime for leg i, between 0 and 1
            
        Returns:
            crt_x, crt_y, crt_z: Coordinates to leg i relative to COM
        '''
        crt_x = sh.Data.com[0]
        crt_y = sh.Data.com[1]
        crt_z = 0
        if sh.Data.support_ratio > 0:
            #for fw movement:
            lapse = ((ct/sh.Data.support_ratio) - sh.Data.distribution)
            crt_x += sh.Data.stride_x * lapse
            crt_y += sh.Data.stride_y * lapse
            #for teta
            crt_teta = sh.Data.teta*lapse #teta changes with ct
            crt_x += -((sh.Data.y_pos[i] * np.sin(crt_teta*np.pi) 
                        + sh.Data.x_pos[i] * np.cos(crt_teta*np.pi))
                        - sh.Data.x_pos[i])
            crt_y += -((sh.Data.x_pos[i]*np.sin(crt_teta*np.pi)
                        - sh.Data.y_pos[i]*np.cos(crt_teta*np.pi)) 
                        + sh.Data.y_pos[i])
        #for delta
        crt_x += -(sh.Data.x_pos[i] * (1.0-np.cos(sh.Data.delta*np.pi)))
        crt_z += -(sh.Data.x_pos[i] * np.sin(sh.Data.delta*np.pi))
        #for rho
        crt_y += -(sh.Data.y_pos[i]*np.cos(sh.Data.rho*np.pi)
                    + sh.Data.hight*np.sin(sh.Data.rho*np.pi)
                    - sh.Data.y_pos[i])
        crt_z += -(sh.Data.hight - (sh.Data.hight*np.cos(sh.Data.rho*np.pi)
                 - sh.Data.y_pos[i]*np.sin(sh.Data.rho*np.pi)))
        #to avoid extreme positions
        if crt_z > (2*sh.Data.leglen - sh.Data.hight)*0.8:
            crt_z = (2*sh.Data.leglen - sh.Data.hight)*0.8
        return crt_x, crt_y, crt_z
    
    def get_cycle_time(phase):
        '''Returns the cycleTime considering the phase'''
        new_time = np.abs(phase+(-1.0))
        cur_cycle_time = 0.0 #between 0 and 1, current Time of cycle
        cur_cycle_time = ((cur_time() - sh.Data.last_cycle_time) 
                            /sh.Data.cycle_time)
        if cur_cycle_time >= 1.0:
            sh.Data.last_cycle_time = cur_time()
            cur_cycle_time = 0
        for i in range(4):
            new_time[i] += cur_cycle_time
            if new_time[i] > 1:
                new_time[i] -= 1
        return new_time
    
    def gait_planning():
        '''
        Determines if a leg is supporting or not considering the current cycle
        time and phase, calculates the coordinates for each leg and ads the 
        shiftment for dodging COM
        
        Returns:
            gp_x, gp_y, gp_z: Numpy-Arrays with coordinates for each leg
        '''
        gp_x = np.array([0.0,0.0,0.0,0.0])
        gp_y = np.array([0.0,0.0,0.0,0.0])
        gp_z = np.array([0.0,0.0,0.0,0.0])
        ct = get_cycle_time(sh.Data.phase)
        for i in range(4):
            if ct[i] < sh.Data.support_ratio:
                gp_x[i], gp_y[i], gp_z[i] = crt(i, ct[i])
            else:
                gp_x[i], gp_y[i], gp_z[i] = beziere(ct[i] 
                                            - sh.Data.support_ratio,
                                            crt(i, sh.Data.support_ratio),
                                            crt(i, 0.0), np.array([0.0,0.0,
                                            -sh.Data.bez_hight*sh.Data.hight]))
        dodge_x, dodge_y = dodge(ct)
        #moving away the body from unloaded legs:
        gp_x += dodge_x
        gp_y += dodge_y
        #tell the simulation to move the upper body
        if sh.Data.simulation_active:
            sh.send_data(("x", dodge_x))
            sh.send_data(("y", dodge_y))
        return gp_x, gp_y, gp_z
    
    gl_x = np.array([0.0, 0.0, 0.0, 0.0])
    gl_y = np.array([0.0, 0.0, 0.0, 0.0])
    gl_z = np.array([0.0, 0.0, 0.0, 0.0])
    gl_x, gl_y, gl_z = gait_planning()
    
    #Move legs to gaits inital position
    if np.any(sh.Data.global_x != gl_x):
        p2 = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0),
              (0.0, 0.0, 0.0)]
        for i in range(4):
            p2[i] = (gl_x[i], gl_y[i], gl_z[i])
        move_legs_to(p2, (0.0, 0.0, -0.4*sh.Data.hight), sh.Data.cycle_time)
    
    while sh.Data.gait_active:  #loop
        #this is where the Magic happens:
        gl_x, gl_y, gl_z = gait_planning()
        f, t, c = get_angles(gl_x, gl_y, gl_z)
        sh.send_data(f, 'f')
        sh.send_data(t, 't')
        sh.send_data(c, 'c')
        #save coordinates globally
        sh.Data.global_x = gl_x
        sh.Data.global_y = gl_y
        sh.Data.global_z = gl_z


def demo():
    '''Used for non-periodic movements, calculates different movements and
    sends to socket/serial indepently'''
    def update_angles(update_x, update_y, update_z, special=None,
                      balance_active=True):
        if balance_active:
            update_x, update_y, update_z = balance(update_x, update_y, update_z)
        f, t, c = get_angles(update_x, update_y, update_z)
        if special is not None:
            leg = special[0]
            if special[1] is 0:
                t[leg] = f[leg] + 90
        sh.send_data(f, 'f')
        sh.send_data(t, 't')
        sh.send_data(c, 'c')
        sh.Data.global_x = update_x
        sh.Data.global_y = update_y
        sh.Data.global_z = update_z
        
    def handshake(ct, start_cycle):
        if cycle is 0:
            demo_y[0] = 0
            demo_z[0] = -sh.Data.hight * 0.8 * ct
            demo_x[0] = -sh.Data.hight * 0.8 * ct
            update_angles(demo_x, demo_y, demo_z, balance_active=True)
        elif cycle is start_cycle + 1:
            demo_y[0] = 0
            demo_z[0] = -sh.Data.hight * 0.8
            demo_x[0] = -sh.Data.hight * (0.8-0.1*ct)
            update_angles(demo_x, demo_y, demo_z, (0,0), balance_active=True)
        elif cycle is start_cycle + 2:
            demo_y[0] = 0
            demo_z[0] = -sh.Data.hight * 0.8
            demo_x[0] = -sh.Data.hight * (0.7+0.1*ct)
            update_angles(demo_x, demo_y, demo_z, (0,0), balance_active=True)
        elif cycle is start_cycle + 3:
            demo_y[0] = 0
            demo_z[0] = -sh.Data.hight * 0.8
            demo_x[0] = -sh.Data.hight * (0.8-0.1*ct)
            update_angles(demo_x, demo_y, demo_z, (0,0), balance_active=True)
        elif cycle is start_cycle + 4:
            demo_y[0] = 0
            demo_z[0] = -sh.Data.hight*0.8
            demo_x[0] = -sh.Data.hight*(0.7+0.1*ct)
            update_angles(demo_x, demo_y, demo_z, (0,0), balance_active=True)
        elif cycle is start_cycle + 5:
            demo_y[0] = 0
            demo_z[0] = -sh.Data.hight * 0.8
            demo_x[0] = -sh.Data.hight * (0.8-0.1*ct)
            update_angles(demo_x, demo_y, demo_z, (0,0), balance_active=True)
        elif cycle is start_cycle + 6:
            demo_y[0] = 0
            demo_z[0] = -sh.Data.hight * 0.8
            demo_x[0] = -sh.Data.hight * (0.7+0.1*ct)
            update_angles(demo_x, demo_y, demo_z, (0,0), balance_active=True)
        elif cycle is start_cycle + 7:
            demo_y[0] = 0
            demo_z[0] = -sh.Data.hight * 0.8 * (1-ct)
            demo_x[0] = -sh.Data.hight * 0.8 * (1-ct)
            update_angles(demo_x, demo_y, demo_z, balance_active=True)
            
    def twerk(ct, start_cycle):
        demo_x = np.array([0.0, 0.0, 0.0, 0.0])
        demo_y = np.array([0.0, 0.0, 0.0, 0.0])
        demo_z = np.array([0.0, 0.0, 0.0, 0.0])
        if cycle is start_cycle:
            demo_x[[0, 1, 2, 3]] = 10.0*ct
        elif start_cycle <= cycle <= start_cycle + 8:
            demo_x[[0, 1, 2, 3]] = 10.0
            demo_z[[2, 3]] = -sh.Data.hight * 0.2 * np.abs(np.sin(3*np.pi*ct))
        elif cycle is start_cycle + 9:
            demo_x[[0, 1, 2, 3]] = 10.0 * (1-ct)
        update_angles(demo_x, demo_y, demo_z)
        
    def rotate(ct, start_cycle, axis):
        #rotate around the z axis
        demo_x = np.array([0.0, 0.0, 0.0, 0.0])
        demo_y = np.array([0.0, 0.0, 0.0, 0.0])
        demo_z = np.array([0.0, 0.0, 0.0, 0.0])
        if cycle is start_cycle:
            angle = 0.02*ct
        elif cycle is start_cycle + 1:
            angle = 0.02*(1-ct)
        elif cycle is start_cycle + 2:
            angle = -0.02*ct
        elif cycle is start_cycle + 3:
            angle = -0.02*(1-ct)
        if axis is 0: #z
            for i in range(4):
                demo_x[i] = -((sh.Data.y_pos[i] * np.sin(angle*np.pi)
                            + sh.Data.x_pos[i] * np.cos(angle*np.pi))
                            - sh.Data.x_pos[i])
                demo_y[i] = -((sh.Data.x_pos[i] * np.sin(angle*np.pi)
                            - sh.Data.y_pos[i] * np.cos(angle*np.pi))
                            + sh.Data.y_pos[i])
        elif axis is 1:#y
            for i in range(4):
                demo_x[i] = -(sh.Data.x_pos[i] * (1.0-np.cos(angle*np.pi)))
                demo_z[i] = -(sh.Data.x_pos[i] * np.sin(angle*np.pi))
        elif axis is 2:#x
            for i in range(4):
                demo_y[i] = -(sh.Data.y_pos[i] * np.cos(angle*np.pi)
                            + sh.Data.hight * np.sin(angle*np.pi) 
                            - sh.Data.y_pos[i])
                demo_z[i] = -(sh.Data.hight
                             - (sh.Data.hight * np.cos(angle*np.pi)
                             - sh.Data.y_pos[i] * np.sin(angle*np.pi)))   
        update_angles(demo_x, demo_y, demo_z)
        
    def schnapDance(ct, start_cycle):
        #do the Schnapdance
        demo_x = np.array([0.0, 0.0, 0.0, 0.0])
        demo_y = np.array([0.0, 0.0, 0.0, 0.0])
        demo_z = np.array([0.0, 0.0, 0.0, 0.0])
        if (cycle-start_cycle)%2 is 0:
            demo_y[[0,1,2,3]] = -20.0 * np.sin(np.pi*ct)
            demo_y[2] *= -1.0
            demo_z[2] = -np.abs(20.0 * np.sin(2.0*np.pi*ct))
        elif (cycle-start_cycle)%2 is 1:
            demo_y[[0,1,2,3]] = 20.0 * np.sin(np.pi*ct)
            demo_y[3] *= -1.0
            demo_z[3] = -np.abs(20.0 * np.sin(2.0*np.pi*ct))
        update_angles(demo_x, demo_y, demo_z, balance_active=False)
        
    def jump(ct):
        demo_x = np.array([0.0, 0.0, 0.0, 0.0])
        demo_y = np.array([0.0, 0.0, 0.0, 0.0])
        demo_z = np.array([0.0, 0.0, 0.0, 0.0])
        for i in range(4):
            if ct < 0.4:
                demo_z[i] = -15 * (ct/0.4)
            elif ct < 0.5:
                demo_z[i] = 6
            else:
                demo_z[i] = 6 * (1-(ct-0.5)/0.5)
        update_angles(demo_x,demo_y,demo_z)
       
    demo_x = np.array([0.0, 0.0, 0.0, 0.0])
    demo_y = np.array([0.0, 0.0, 0.0, 0.0])
    demo_z = np.array([0.0, 0.0, 0.0, 0.0])
    sh.Data.gait_active = False
    demo_time = cur_time()
    cycle = 0
    
    
    sh.Data.gait_active = True
    while sh.Data.gait_active:
        #resetting the current values to prevent wrong calculations:
        demo_x *= 0.0
        demo_y *= 0.0
        demo_z *= 0.0
        ct = (cur_time()-demo_time) / sh.Data.cycle_time
        if ct >= 1:
            ct = 0
            demo_time = cur_time()
            cycle += 1
        #instructions per cycle:
        #jump
        '''
        if 0 <= cycle <= 8:
            jump(ct)
        elif cycle is 9:
            break
        '''
        '''
        #schnapdance
        if 0 <= cycle <= 8:
            schnapDance(ct,0)
        elif cycle is 9:
            break
        '''    
        '''
        #rotate
        if 0 <= cycle <= 3:
            rotate(ct,0,0)
        if 4 <= cycle <= 7:
            rotate(ct,4,1)
        if 8 <= cycle <= 11:
            rotate(ct,8,2)
        elif cycle is 12:
            break
        '''
        '''
        #twerk
        if 0 <= cycle <= 9:
            twerk(ct,0)
        elif cycle is 10:
            break
        '''
        #'''
        #handshake
        if 0 <= cycle <= 7: 
            handshake(ct, 0) #takes cycle 0 to 7
        elif cycle is 8:
            break
        #'''
        time.sleep(0.001)
    print "finished demo!"
   
     
def calibrate_com():
    '''Loop thats searches for the optimal COM. The robot moves with zero
    stride and changing COM-settings. The algorithm gets the acceleration
    a sensor measusres and searches for the COM with the least instability.
    
    No args or returns. The loop-thread stops if calibration is finished and 
    stores the resulting new COM values in the shared Data.
    '''
    import threading
    print "setting up, please wait..."
    #setting up global requirements, hopping without forward movement
    sh.Data.data_logging = True
    sh.Data.calc_com_active = False
    sh.Data.gait_active = False
    #safe strides to restore if calibration finished
    old_stride_x = sh.Data.stride_x+0.0
    old_stride_y = sh.Data.stride_y+0.0
    sh.Data.stride_x = 0.0
    sh.Data.stride_y = 0.0
    sh.Data.phase = np.array([0.75, 0.25, 0.25, 0.75])
    sh.Data.gait_active = True
    GaitLoop = threading.Thread(target=gait_loop,)
    GaitLoop.start()
    
    def calibration_loop(axis):
        best_result = 1e10
        measure_range = 10
        result = np.array([0.0, 0.0, 0.0])
        best_com = np.array([0.0, 0.0])
        com = np.array([0.0, 0.0, 0.0, 0.0])
        print "#" + "\t" + "mean" + "\t\t" + "best mean" + "\t" + "best COM"
        for n in range(-measure_range, measure_range+1):
            com[axis] = n
            for i in range(2):
                #stop calibration if global stopgait
                if not sh.Data.gait_active:
                    return
                time.sleep(sh.Data.cycle_time/1000.0) #do a whole cycle
                #sum all accelerations in y and x direction
                #data-intervall MUST be one cycle
                result[i] = (np.var(sh.Data.data_acc_x)
                            + np.var(sh.Data.data_acc_y))
            #mean the acceleration of all cycles
            mean = round(np.mean(result))
            #compare accelerations and check if there has been a better one yet
            if mean < best_result:
                best_result = mean
                best_com[axis] = n
            print str(n) + "\t" + str(mean) + "\t\t" + str(best_result)\
                  + "\t\t" + str(best_com[axis])
        sh.Data.com[axis] = best_com[axis]
            
    time.sleep(3*sh.Data.cycle_time/1000.0) #wait until move_legs_to finishes
    #change and measure comx
    print "\ncalibrating com_x"
    calibration_loop(0)
    if not sh.Data.gait_active:
        return
    print "\ncalibrating com_y"
    calibration_loop(1)
    sh.Data.gait_active = False
    move_legs_to([(0.0, 0.0, -50.0), (0.0, 0.0, 0.-50), (0.0, 0.0, -50.0),
                  (0.0, 0.0, -50.0)]) #get down
    sh.Data.calc_com_active = True
    sh.Data.stride_x = old_stride_x
    sh.Data.stride_y = old_stride_y
    print "\ncalibration finished, changed COM to", sh.Data.com
    
   
def move_legs_to(p2 = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0)],p1 = (0.0, 0.0, -0.4*sh.Data.hight),
                duration=5000.0):
    '''
    Moves legs from their current position to point p2 with p1 as the vertex
    
    Args: 
        p2: end point of movement (set of coordinates for each leg)
        p1: vertex of movement
        duration: time in ms to move from current point to p2
    '''
    x = np.array([0.0, 0.0, 0.0, 0.0])
    y = np.array([0.0, 0.0, 0.0, 0.0])
    z = np.array([0.0, 0.0, 0.0, 0.0])
    last_time = cur_time()
    #write current leg positions to p0:
    p0 = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)]
    for i in range(4):
            p0[i] = (sh.Data.global_x[i], sh.Data.global_y[i],
                      sh.Data.global_z[i])   
    #loop
    while (cur_time()-last_time) < duration :
        for i in range(4):
            x[i], y[i], z[i] = beziere(cur_time()-last_time, p0[i], p2[i],
                                       p1 ,duration)
        f, t, c = get_angles(x, y, z)
        sh.send_data(f, 'f')
        sh.send_data(t, 't')
        sh.send_data(c, 'c')
    #save current leg positions
    sh.Data.global_x = x
    sh.Data.global_y = y
    sh.Data.global_z = z


def shun():
    '''Set every angle to zero. Used for testing the joints zero-positions.'''
    sh.Data.gait_active = False
    for joint in ['f', 't', 'c']:
        sh.send_data(np.array([0.0, 0.0, 0.0, 0.0]), joint)
    print "Aye Sir!"
 
           
def set_zero_pos():
    '''
    Menu to set new zero-positions for each joint and save them to
    Arduino EEPROM.
    '''
    shun()
    print "\n+------------------+\n|   ZEROPOS-MENU   |\n+------------------+"
    print "Change the zeroPos of every joint\n"\
         +"Exit the menu:\t\tquit\n"\
         +"Choose the joint:\tf/t/c\n"\
         +"Choose the leg:\t\t0/1/2/3\n"\
         +"In/decrase zeroPos:\t+/-\n"
    joint = 't'
    leg = '0'
    while True:
        inp = raw_input("[zeroPos][" + joint + leg + "]-> ")
        if inp in ["n","q","quit"]:
            print "Do you want to save the changes? y/n"
            while True:
                inp = raw_input("[zeroPos]-> ")
                if inp is "y":
                    sh.send_data(('u',None))       #update values to EEPROM
                    print "zero_pos saved!"
                    break
                elif inp in ["n","q","quit"]:
                    break
                else:
                    print "There is no command: ",inp
            shun()
            break
        elif inp in ['f', 't', 'c']:
            joint = inp
        elif inp in ['0', '1', '2', '3']:
            leg = inp
        elif inp in ["+","-"]:
            sh.send_data(("z" + joint + leg, (2.0 if inp is "+" else 0.0)))
        else:
            print "There is no command: ", inp