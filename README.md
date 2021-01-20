# Quaro Quadruped Robot v3
Planning- and control-software for Quadrupedal Robots.

This is the third iteration of my quadruped robot. As it is still in development, some files in this repository are still missing and some pictures are are out of date. However my goal is to upload all new files as soon as possible!

The robot uses a Raspberry Pi for control and an Arduino Mega 2560 for handling the hardware.

![diagram](https://github.com/ThomasSchnapka/quaro/blob/v3/doc/Quaro_diagramm.png)

![hardware](https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/doc/hardware_image.jpg)

---
Update 20.01.2020

Today I found the reason why the servos were jittering sometimes. Although I bought high torque servos, it seems that they were not capable of handling the robots weight in the long run. One IC is burned on most of the servos.

![burnt servo](https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/doc/burnt_servo.jpeg)

There are two things I can do right now: 1) buy new similar servos and limit the robots movements so that the current will stay low or 2) find a way to build the robot with other motors than RC servos.

Since a limitited robot is a boring one, I will focus on the second option. The main problem here is that all of-the-shelf-servos that fit my budget run on low voltages. As exactly this is my problem (low voltage -> high current -> burnt servos) I have to find another way to realize the robots actuators. Let's see how long this will take. 
