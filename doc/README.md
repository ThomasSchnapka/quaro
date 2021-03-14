# Quaro Documentation

* [Basic structure of control workflow](#basic-structure)
* [Inclination Control](#inclination_control)
* [Forward kinematics](#forward-kinematics)

## Basic structure of control workflow

![basic structure](https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/doc/quaro_main_workflow.png)

## Inclination Control

### Introduction

The robot is able to walk on surfaces with a certain inclination using a controller that changes the position of the center of mass based on the inclination. The following two videos show the robot walking a slope without and with inclination control.

<p float="left">
  <img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/media/walking_without_inclination_control.gif" width="250">
  <img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/media/walking_with_inclination_control.gif" width="250">
</p>

### Realization

<img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/doc/inclination_control_explaination.png" width="300">

The inclination control problem can be seen as an inverted pendulum. The goal is to keep the center of mass above the projection of the COM between the legs. This is done by rotating the body around this projection. The corresponding control loop is:


![inclination_control_loop](https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/doc/inclination_control_loop.png)

A big difference to the "classical" inverted pendulum problem is that the position of the robot can only be altered by changes in the angle theta, the resulting torque itself is not controllable. Therefore the change in angle gets converted into a torque inside the control loop [1]. Other acting torques are the damping force as well as the moment of inertia [2].

The disturbance in this case is the change in inclination (the slope). The robots orientation gets determined by calculating the direction of gravity using an IMU. Because of the non-ideal gait movement (the "body wobble"), the measurements contain parasitic accelerations. To suppress them, the IMU measurements get filtered by a low pass filter with a cut off frequency below (1/cycle_time) [3].


## Forward kinematics

![Fordward Kinematics](https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/doc/Quaro_Kinematics.png)
