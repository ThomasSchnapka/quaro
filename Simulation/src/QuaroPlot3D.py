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

Last version of QuaroPlot3D drawed the axes entirely new in each cycle 
deleting the old one using plt.cla(). Although this is a pretty
easy solution, it was very slow. The new version changes the matplotlib axes 
instead of recreating them.
"""


import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3D
from matplotlib.animation import FuncAnimation
import numpy as np
from IPython import get_ipython

from src import forward_kinematics



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
    
    
    def update_plot(self, i, leg_lines, body_lines, leg_numbers,
                    stability_triangle, com_projection):
        '''
        animation function that gets called repeatedly and updates plot
        
        Parameters
        ----------
        i : int, iterable to that gets passed by FuncAnimation, not used here
        leg_lines : matplotlib line3D objects that gets altered
        body_lines : matplotlib line3D objects that gets altered
        leg_numbers : matplotlib text3D objects that gets altered
        stability_triangle : matplotlib line3d object that gets altered
        com_projection : matplotlib line3d object that gets altered

        Returns
        -------
        None.

        '''
        
        ## retrieve robot state
        joint_angles = self.data_source.request_data("joiang")
        rpy = self.data_source.request_data("ropiya")
        
        ## retrieve points representing the robots pose
        leg_points = forward_kinematics.full_leg_coordinates(joint_angles, rpy)
        edges = forward_kinematics.body_edges(rpy)
        
        ## plot legs and leg numbers
        for n in range(4):
            leg_lines[n].set_data_3d(leg_points[n,0,:],
                                     leg_points[n,1,:],
                                     leg_points[n,2,:])
            # plot leg numbers
            leg_numbers[n].set_position((edges[0, n], edges[1, n]))
            leg_numbers[n].set_3d_properties(edges[2, n] - 30)
        
        ## plot stability triangle
        ground_points = leg_points[:,:-1,-1].T
        # points of legs that touch the ground
        lowest_coordinate = np.max(ground_points[-1])
        leg_on_ground = np.abs(ground_points[2]-lowest_coordinate) < 5 #tolerance
        ground_points = ground_points[:, leg_on_ground]
        # check if there is more than one ground points to draw something
        if ground_points.shape[1] > 1:
            # add a point to plot a closed curve
            ground_points[:,[0,1]] = ground_points[:,[1, 0]]
            ground_points = np.vstack((ground_points.T, ground_points[:,0])).T
            stability_triangle.set_data_3d(ground_points[0],
                                           ground_points[1],
                                           ground_points[2])
        else:
            # show no stability polygon if no leg on ground
            stability_triangle.set_data_3d(0,0,0)
        
        ## plot projection of COM onto ground
        com_projection.set_data_3d([0, 0],
                                   [0, 0],
                                   [0, lowest_coordinate])
        
        ## plot body   
        # swap 2 and 3 coordinate so that connecting lines do not cross in plot
        edges[:,[0,1]] = edges[:,[1, 0]]
        # add collumn to body edges to plot a closed curve
        edges = np.hstack((edges, edges))[:,:-3]
        
        body_lines.set_data_3d(edges[0], edges[1], edges[2])
        
    
    def start_plot(self):
        '''Initialize Plot'''
        # set axes properties
        ax_range = 230
        self.ax.set_xlim3d([-ax_range, ax_range])
        self.ax.set_ylim3d([-ax_range, ax_range])
        self.ax.set_zlim3d([-ax_range, ax_range])
        self.ax.set_xlabel("x", fontsize=14, fontweight='bold')
        self.ax.set_ylabel("y", fontsize=14, fontweight='bold')
        self.ax.set_zlabel("z", fontsize=14, fontweight='bold')
        
        # create right handed coordinate system
        self.ax.invert_yaxis()
        self.ax.invert_zaxis()
        
        # create empty matplotlib plot objects
        leg_lines = [self.ax.plot(0,0,0,color="black")[0] for n in range(4)]
        body_lines = self.ax.plot(0,0,0, color="blue", linewidth=3)[0]
        leg_numbers = [self.ax.text(0,0,0, str(n)) for n in range(4)]
        stability_triangle = self.ax.plot(0,0,0,color="red")[0]
        com_projection = self.ax.plot(0,0,0,'o-',color="red")[0]
        
        # create animation
        ani = FuncAnimation(self.fig, self.update_plot,
                            fargs=(leg_lines, body_lines, leg_numbers,
                            stability_triangle, com_projection), interval=50)
        plt.show(block=True)
        print("[QuaroPlot3D] animation started! To stop the script, you",
              "MUST close the figure window!")
        return ani
        
 
        
        
#---------------------------- standalone test -------------------------------#

if __name__ == "__main__":
    
    # create data source dummy
    class TestDataSource:
        def request_data(self, typ):
            if typ == "joiang":             # joint angles
                angles = np.array([[ 27.54812251, -42.0457834,   27.54812251, -42.0457834 ],
                                   [-50.14377845,  75.85203445, -50.14377845,  75.85203445],
                                   [-33.05519517,   5.21860477, -33.05519517,   5.21860477]])
                return angles
            elif typ == "ropiya":           # pitch roll yaw angeles
                return np.array([0, 0, 20])
            
    tds = TestDataSource()
    qp3 = QuaroPlot3D(tds)
    ani = qp3.start_plot()
    #ani.save("ani.gif")