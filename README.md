# Quaro Quadruped Robot v4
Control software for quadrupedal robots with a focus on tidy kinematics and motion. Made by Thomas Schnapka.

### General
This repo contains the control software that runs my version of KDY0523's [SpotMicro](https://www.thingiverse.com/thing:3445283). 

#### capabilities:
* parameterizable gait generator
* maintains stability _(so far only static stability is considered)_
* state visualization for testing and during robot operation
* servo protection
* interactive menu

All scripts are written in Python. The code is highly vectorized, thus I think it would make little to no difference to port some parts into C++. However I did not check this yet.


### Installation note

As this repo contains a submodule, it is necessary to use clone it with
the `--recurse-submodules` option:

```
git clone --branch v4 --recurse-submodules https://github.com/ThomasSchnapka/quaro.git
```

### Hardware
* Raspberry Pi 3
* 12 JX HV5932MG Servos
* PCA9685 servo board

### Future work
- [] implement (inverse) dynamic model
- [] implement IMU support
- [] add foot contact switches similar to [these here](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/foot_contact_switch_v1/README.md)
- [] add a nice blinking light

long term:
- [] buy [better actuators](https://mjbots.com/) that can handly higher loads and give sensor feedback to enable closed loop control

### Additional resources 
[mikes4192's version of spotMicro built with ROS and supporting SLAM](https://github.com/mike4192/spotMicro)
[Open Dynamic Robot Initiative with a focus on research](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware)
[michaelkubina's version of spotMirco using an ESP32](https://github.com/michaelkubina/SpotMicroESP32/#bill-of-material)
