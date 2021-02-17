#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a 3D animation of robots legs

Please be aware of the fact that matplotlibs FuncAnimation MUST be called by
the main programm and blocks it. This can be circumvented using several 
processes.

To stop this script, the plot window MUST be closed, otherwise the connection
to the robot server will not be closed properly

If plot does not show up, use the %matplotlib qt command in IPython

"""


import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3D
from matplotlib.animation import FuncAnimation
import numpy as np
from IPython import get_ipython

import forward_kinematics


# open plot in new window instead of inline
# use %matplotlib qt if plot is not showing up
get_ipython().run_line_magic('matplotlib', 'qt')



class QuaroPlot3D:
    
    
    def __init__(self, data_source):
        '''
        initalizes plot object
        
        Parameters
        ----------
        data_source: PlotDataClient which connects with robot server
        
        '''
        
        # create plot class
        self.data_source = data_source
        
        # create plot
        self.fig = plt.figure()
        self.ax = axes3D.Axes3D(self.fig)
        self.ax.set_title('Quaro Simulation')
        
        
        
    def set_ax_properties(self):
        '''as plt.cla() is used in animation and deletes the axes properties,
        they have to be reset again every time'''
        # Setting the axes properties
        boundary = 200
        self.ax.set_xlim3d([-boundary, boundary])
        self.ax.set_ylim3d([-boundary, boundary])
        self.ax.set_zlim3d([-boundary, boundary])
        self.ax.set_xlabel("x", fontsize=14, fontweight='bold')
        self.ax.set_ylabel("y", fontsize=14, fontweight='bold')
        self.ax.set_zlabel("z", fontsize=14, fontweight='bold')
        
        # create right handed coordinate system
        self.ax.invert_yaxis()
        self.ax.invert_zaxis()
    
    
    def animate(self, i):
        '''this function gets called repeatedly and updates animation'''
        
        # clear axes and reset axes properties
        plt.cla()
        self.set_ax_properties()
        
        # retrieve robot state
        joint_angles = self.data_source.request_data("joiang")*(2*np.pi/360)
        rpy = self.data_source.request_data("ropiya")*(2*np.pi/360)
        
        # retrieve points representing the robots pose
        leg_points = forward_kinematics.full_leg_coordinates(joint_angles, rpy)
        edges = forward_kinematics.body_edges(rpy)
        
        # plot legs
        for n in range(4):
            self.ax.plot(leg_points[n][0,:],
                         leg_points[n][1,:],
                         leg_points[n][2,:],
                         color="black")
            self.ax.text(edges[0, n], edges[1, n], edges[2, n], str(n))
       
        # plot body
        # swap 2 and 3 coordinate so that connecting lines do not cross in plot
        edges[:,[0,1]] = edges[:,[1, 0]]
        # add collumn to body edges to plot a closed curve
        edges = np.hstack((edges, edges))[:,:-3]
        self.ax.plot(edges[0], edges[1], edges[2], color="blue")
        
    
    def start_plot(self):
        '''Initialize Plot'''
        self.ani = FuncAnimation(self.fig, self.animate, interval=50)
        
        #plt.ion()
        plt.show(block=True)
        print("[QuaroPlot3D] animation started! To stop the script, you",
              "MUST close the figure window!")
        
 
        
        
#---------------------------- standalone test -------------------------------#

if __name__ == "__main__":
    
    # create data source dummy
    class TestDataSource:
        def request_data(self, typ):
            if typ == "joiang":             # joint angles
                return np.zeros((3,4))
            elif typ == "ropiya":           # pitch roll yaw angeles
                return np.zeros(3)
            
    tds = TestDataSource()
    qp3 = QuaroPlot3D(tds)
    ani = qp3.start_plot()
    #ani.save('test.gif')
    
