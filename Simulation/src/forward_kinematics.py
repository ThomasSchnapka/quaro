#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Forward Kinematics for Quaro quadruped robot. This script tries to match the
real behavior of the robot as close as possible. This is the transformations
are not done using the DH-convention because the DH-requirements are not met
due to the coordinate system defined by the robot controller

Explaination of defintions can be found in "Quaro_Kinematics.svg"
"""

## imports and redefinitions
import numpy as np
# redefine some functions for better visualisation in code
sin = np.sin
cos = np.cos
tan = np.tan
sqrt = np.sqrt
pi = np.pi


## Geometric definitions (in mm)
a = 186     # body length
b = 78      # body width
h = 11      # vertical shoulder displacement
g = 55      # horizontal shoulder displacement
l1 = 108    # upper leg length
l2 = 130    # lower leg length

leg_location = np.array([[ (a/2),  (a/2), -(a/2), -(a/2)],
                         [-(b/2),  (b/2), -(b/2),  (b/2)],
                         [     0,      0,      0,      0]])

## transformation equations

def rot_z(angle):
    return np.array([[cos(angle), -sin(angle),           0,           0],
                     [sin(angle),  cos(angle),           0,           0],
                     [         0,           0,           1,           0],
                     [         0,           0,           0,           1]])
def rot_x(angle):
    return np.array([[         1,           0,           0,           0],
                     [         0,  cos(angle), -sin(angle),           0],
                     [         0,  sin(angle),  cos(angle),           0],
                     [         0,            0,          0,           1]])

def rot_y(angle):
    return np.array([[ cos(angle),            0,  sin(angle),           0],
                     [          0,            1,           0,           0],
                     [-sin(angle),            0,  cos(angle),           0],
                     [          0,            0,           0,           1]])

def trans(x, y, z):
    return np.array([[          1,            0,           0,           x],
                     [          0,            1,           0,           y],
                     [          0,            0,           1,           z],
                     [          0,            0,           0,           1]])

def rot_rpy(roll, pitch, yaw):
    return rot_z(roll)@rot_y(pitch)@rot_y(yaw)


## transformation equations for quadruped robot
    
def single_leg_coordinates(leg_num, angles):
    '''
    Returns leg coordinates with leg shoulder as base coordinate system

    Parameters
    ----------
    leg_num : int, number of leg as defined in "Quaro_Kinematics.svg"
    angles : (3x1) numpy.ndarray,  alpha, beta, gamma angles in RAD

    Returns
    -------
    (3,8) numpy.ndarray of 8 points representing the transformation chain in
          x/y/z-coordinates

    '''
    T_0_1 = rot_z(pi*(leg_num%2))     # leg 1 and 3 are rotated
    T_1_2 = rot_x(angles[2])
    T_2_3 = trans(0, 0, h)
    T_3_4 = trans(0, -g, 0)
    T_4_5 = rot_y(angles[0])
    T_5_6 = trans(0, 0, l1)
    T_6_7 = rot_y(angles[1])
    T_7_8 = trans(0, 0, l2)
    
    transformations = [T_0_1, T_1_2, T_2_3, T_3_4, T_4_5, T_5_6, T_6_7, T_7_8]

    # calculate all points of kinematic chain
    # (numpy uses @ for matrix- and * for elementwise-multiplication)
    chain = np.zeros((len(transformations)+1, 4))
    origin = np.array([0, 0, 0, 1])
    chain[0] = origin
    # other transformations
    T = np.zeros((4, 4))
    T[range(4), range(4)] = 1
    for i, T_next in enumerate(transformations):
        T = T@T_next
        chain[i+1] = T@origin
    return chain.T


def all_leg_coordinates(angles):
    '''
    returns coordinates of all four legs transformed to their position
    
    base coordinate system is body coordinate system (without considering
    pitch, roll and yaw of body)

    Parameters
    ----------
    angles : (3x4) numpy.ndarray,  alpha, beta, gamma in RAD of all four legs
                                   (same as returned by robot controller)

    Returns
    -------
    (4,3,8) numpy.ndarray, points representing the leg coordinates

    '''
    coordinates = [0,0,0,0]
    for leg_num in range(4):
        chain = single_leg_coordinates(leg_num, angles[:, leg_num])
        # leg location
        chain = trans(leg_location[0, leg_num],
                      leg_location[1, leg_num],
                      leg_location[2, leg_num])@chain
        coordinates[leg_num] = chain
    return np.array(coordinates)


def full_leg_coordinates(angles, rpy):
    '''
    returns coordinates of all four legs considering roll, pitch, yaw
    
    base coordinate system is COM coordinate system

    Parameters
    ----------
    angles : (3x4) numpy.ndarray,  alpha, beta, gamma in RAD of all four legs
                                   (same as returned by robot controller)
    rpy : (3x1) numpy.ndarray,  roll, pitch, yaw in RAD (as returned by 
                                                         robot controller).

    Returns
    -------
    (4,3,8) numpy.ndarray, points representing the leg coordinates

    '''
    coordinates = all_leg_coordinates(angles)
    T_COM_b = rot_rpy(rpy[0], rpy[1], rpy[2])
    for leg_num in range(4):
        coordinates[leg_num] = T_COM_b@coordinates[leg_num]
    return coordinates


def body_edges(rpy):
    '''
    Returns edges of body for visualisation

    Parameters
    ----------
    rpy : (3x1) numpy.ndarray,  roll, pitch, yaw in RAD (as returned by 
                                                         robot controller).
    Returns
    -------
    (3,4) numpy.ndarray with coordinates off body corners

    '''
    corners = np.vstack((leg_location, np.ones(4)))
    T_COM_b = rot_rpy(rpy[0], rpy[1], rpy[2])
    corners = T_COM_b@corners
    return corners[:-1]


#---------------------------- standalone test -------------------------------#

if __name__ == "__main__":
    # for testing the module
    
    # set robot pose
    angles = np.zeros((3,4))
    rpy = np.array([pi/8, 0, 0])
    
    ## get data
    legs = full_leg_coordinates(angles, rpy)
    edges = body_edges(rpy)
    
    ## plot setting
    import matplotlib.pyplot as plt
    # use %matplotlib qt if plot is not showing up
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Setting the axes properties
    max_scale = 200
    ax.set_xlim3d([-max_scale, max_scale])
    ax.set_xlabel('X')
    ax.set_ylim3d([-max_scale, max_scale])
    ax.set_ylabel('Y')
    ax.set_zlim3d([-max_scale, max_scale])
    ax.set_zlabel('Z')
    # invert y axis to make the coordinate system right handed
    ax.set_title('3D Test')
    # create right handed coordinate system
    ax.invert_yaxis()
    ax.invert_zaxis()
    
    # plot legs
    for i in range(4):
        ax.plot(legs[i][0,:], legs[i][1,:], legs[i][2,:])
        ax.text(leg_location[0, i], leg_location[1, i],
                leg_location[2, i], str(i))
   
    # plot body
    # add collumn to body edges to plot a closed curve
    edges = np.hstack((edges, edges))[:,:-3]
    ax.plot(edges[0], edges[1], edges[2])
    
    plt.tight_layout()
    plt.show()