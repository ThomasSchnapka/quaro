# Quaro Quadruped Robot
Control software for quadrupedal robots with a focus on tidy kinematics and motion.


<p float="left">
  <img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/v4/media/gif_rpy.gif">
  <img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/v4/media/hardware_image_side.jpeg" width="250">
</p>

_Made by user Thomas Schnapka_


### General
This repo contains the control software that runs my version of KDY0523's [SpotMicro](https://www.thingiverse.com/thing:3445283). 


#### capabilities:
* parameterizable gait generator
* maintains stability _(so far only static stability is considered)_
* servo protection
* interactive menu
* simulation and state visualization for testing and during robot operation

![gif RPY simulation](https://raw.githubusercontent.com/ThomasSchnapka/quaro/v4/media/RPY_simulation.gif) 

All scripts are written in Python. The code is highly vectorized, thus I think it would make little to no difference to port some parts into C++. However, I did not check this yet.


### Hardware
* Raspberry Pi 3
* 12 JX HV5932MG Servos
* PCA9685 servo board
* customized [SpotMicro](https://www.thingiverse.com/thing:3445283) parts with [shoulder reinforcements](https://www.thingiverse.com/thing:4591999).


### Gait
The robot follows the conventions introduced in this [book](https://mitpress.mit.edu/books/legged-robots-balance) by Marc Raibert. The robot's gait can be altered in the `state.py` module by changing each leg's individual phase. If everything works right and the values are not in an extreme region, the control software should be able to maintain stability on its own.

<img src="https://github.com/ThomasSchnapka/quaro/blob/v4/media/gif_walking.gif">

### structure of this repo

```
quaro
│
├── Raspberry
│   ├── main.py
│   ├── src         # general functionalities that can be applied on all quadruped robots
│   │    └── ...
│   └── quaro       # hardware specific functionalities for this certain robot
│        └── ...
│
├── Simulation      # plot of the robots state
│    └── main.py
│
├── doc             # definitions
│
├── media           # images and videos
```
If you want to adopt this software for your own robot, you have to change the hardware-specific parameters in `quaro/hardware_config.py`. Changes for the robot operations are made in `src/state.py` 

### Installation note

As this repo contains a submodule, it is necessary to use clone it with
the `--recurse-submodules` option:

```
git clone --branch v4 --recurse-submodules https://github.com/ThomasSchnapka/quaro.git
```

### Future work
- [ ] add a block diagram about the control software workflow in this repo
- [ ] implement (inverse) dynamic model
- [ ] implement IMU support
- [ ] add foot contact switches similar to [these here](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/foot_contact_switch_v1/README.md)
- [ ] add a nice blinking light

_long term:_
- [ ] buy [better actuators](https://mjbots.com/) that can handle higher loads and give sensor feedback to enable closed-loop control


### Additional resources 
1. book with basics and definitions this software follows [link](https://mitpress.mit.edu/books/legged-robots-balance)
1. Open Dynamic Robot Initiative with a focus on research [link](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware)
1. version of spotMicro by mikes4192 built with ROS and supporting SLAM [link](https://github.com/mike4192/spotMicro)
1. version of spotMirco by michaelkubina using an ESP32 [link](https://github.com/michaelkubina/SpotMicroESP32/)
