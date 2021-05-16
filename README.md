# Quaro Quadruped Robot
Control software for quadrupedal robots with a focus on tidy kinematics and motion. Includes sensor feedback


<p float="left">
  <img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/media/gif_rpy.gif">
  <img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/media/hardware_image_side.jpeg" width="250">
</p>


## Overview
This repo contains the control software that runs my version of KDY0523's [SpotMicro](https://www.thingiverse.com/thing:3445283). 
* [Gait generation](#gait)
* [Structure of this repo](#structure)
* [Installation and execution](#installation-and-execution)
* [Future work](#future-work)
* [Hardware](#hardware)
* [Additional resources](#additional-resources)

### Features:
* parameterizable gait generator
* maintains stability
  * static stability
  * stability during slopes
  * walking on "uneven" terrain using foot contact switches  
* servo protection
* interactive menu
* simulation and state visualization for testing and during robot operation

![gif RPY simulation](https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/media/RPY_simulation.gif) 

The code if mainly written in Python, some parts (where speed matters) are rewritten to C++. I plan to convert most of the code successively and let only the high level control stay in Python. 


## Gait generation
The robot follows the conventions introduced in this [book](https://mitpress.mit.edu/books/legged-robots-balance) by Marc Raibert. The robot's gait can be altered in the `state.py` module by changing each leg's individual phase. If everything works right and the values are not in an extreme region, the control software should be able to maintain stability on its own.

<img src="https://github.com/ThomasSchnapka/quaro/blob/master/media/walking_with_inclination_control.gif" width="500">

## Structure of this repo

```
quaro
│
├── Raspberry        # software running on Raspberry Pi
│   ├── main.py
│   ├── src          # general functionalities that can be applied on all quadruped robots
│   │    └── cpp     # parts written in C++
│   │         └── ...
│   └── quaro        # hardware specific functionalities for this certain robot
│        └── ...
│
├── Arduino          # script for foot contact switch sensors
│
├── Simulation       # plot of the robots state
│    └── main.py
│
├── doc              # definitions
│
├── media            # images and videos
```
If you want to adopt this software for your own robot, you have to change the hardware-specific parameters in `quaro/hardware_config.py`. Changes for the robot operations are made in `src/state.py` 

## Installation and execution
### Installation

_If you just want a simple, reliable quadruped control software in pure Python, download v3.1. The current version is rather a playground for my own experiments and sometimes unstable. (But it contains some cool features though)_

Because this repo contains a submodule, it is necessary to use clone it with
the `--recurse-submodules` option:

```
git clone --branch v4 --recurse-submodules https://github.com/ThomasSchnapka/quaro.git
```
It is no problem to install the software without IMU, PWM-board or any hardware at all. The software detects which hardware is connected and creates a dummy instance if necessary.

### Execution
The menu looks like this:
```
==============================================================
+------------------+
|    QUARO-MENU    |
+------------------+
--------------------------------------------------------------
support_ratio: 0.85            phase:         [0.  0.5 0.5 0. ]
cycle_time:    1500.0          velocity:      [0. 0.]
stab'_ratio:   0.5             rpy:           [0. 0. 0.]
op'_hight:     0.9             true_com:      [-28   0   0]
shoulder_dis': 1               swing_h'_fact':0.95
server_status':True            ang'_velocity':0.0
stab'_ampl':   15             
--------------------------------------------------------------
[QuaroServer] started server at 127.0.0.1 1276
[UserInterface] waiting for commands. Type 'h' for help.
[UserInterface]-> 
```
Most parameters can be changed during runtime. They are changed with `change [parameter-name] [value]`. Type in `h` as command to display the help. Please note that the values you provide are *not checked for validity*. However, the software should prevent damage to your robot as all servo angles are sanity checked. But there is no protection for resulting scratches.


## Future work
- [x] add a block diagram about the control software workflow in this repo
- [x] implement IMU to close control loop
  - [x] controlled slope walking
- [x] add foot contact switches similar to [these](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/foot_contact_switch_v1/README.md)
  - [x] develope a reliable way to sense foot contact while keeping the SpotMicro design
  - [x] be able to walk on uneven terrain 
- [ ] implement dynamic model for [Model Predictive Control](https://de.wikipedia.org/wiki/Model_Predictive_Control)
  - [x] understand MPC by building and controlling an inverted pendulum
  - [ ] do offline trajectory optimization to counteract the inconvenient servo locations
- [x] add a nice blinking light

_long term:_
- [ ] buy [better actuators](https://mjbots.com/) that can handle higher loads and give sensor feedback to enable closed-loop control
- [ ] build a big version


## Hardware
* Raspberry Pi 3
* 12 JX HV5932MG Servos
* PCA9685 servo board
* MPU6050 IMU
* customized [SpotMicro](https://www.thingiverse.com/thing:3445283) parts with [shoulder reinforcements](https://www.thingiverse.com/thing:4591999)

_optional for foot contact switches:_
* customized [legs](https://www.thingiverse.com/thing:4821239)
* Arduino Nano
* Force Sensible Resistors (FSR)
* additional electronics

### Foot Contact Switches

![gif foot contact switches](https://github.com/ThomasSchnapka/quaro/blob/master/media/foot_contact_switches_gait.gif?raw=true)

One of the biggest flaws of a quadruped robot on a budget is that the servo motors do not give any feedback. To deal with it I wanted to try out foot contact switches.
After testing [this approach](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/foot_contact_switch_v1/README.md) with Phototransistors, I found out that using force-sensitive resistors is more feasible if one wants to maintain the Spot Micro design and avoid buying SMD boards. Instructions and files are available on [Thingiverse](https://www.thingiverse.com/thing:4821239). More information: [link](https://github.com/ThomasSchnapka/quaro/tree/master/Hardware/Foot_contact_switch)

## Additional resources 
1. book with basics and definitions this software follows [link](https://mitpress.mit.edu/books/legged-robots-balance)
1. Open Dynamic Robot Initiative with a focus on research [link](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware)
1. version of spotMicro by mikes4192 built with ROS and supporting SLAM [link](https://github.com/mike4192/spotMicro)
1. version of spotMirco by michaelkubina using an ESP32 [link](https://github.com/michaelkubina/SpotMicroESP32/)
