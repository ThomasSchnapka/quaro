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

from src.PlotDataClient import PlotDataClient
from src.QuaroPlot3D import QuaroPlot3D

# create server client
plot_data_client = PlotDataClient()

# start plot is server is running
if plot_data_client.server_running == True:
    plot = QuaroPlot3D(plot_data_client)  
    # this functions runs as long as plot window is open
    ani = plot.start_plot()
    plot_data_client.close()