#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Illustrates the movement calculated by the Quaro robot controller in a three
dimensional Matplotlib animation

Changes concerning the robot geometry can be done in forward_kinematics.py

To stop this script, the plot window MUST be closed, otherwise the connection
to the robot server will not be closed properly

If plot does not show up, use the %matplotlib qt command in IPython
"""

from PlotDataClient import PlotDataClient
from QuaroPlot3D import QuaroPlot3D

# create objects for server connection and plotting
plot_data_client = PlotDataClient()
qp3 = QuaroPlot3D(plot_data_client)    

# start plot
ani = qp3.start_plot()

# close connection with server tidily
plot_data_client.close()