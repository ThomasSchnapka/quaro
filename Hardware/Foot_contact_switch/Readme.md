### Foot contact switch

Printing files and instructions can be found here:
https://www.thingiverse.com/thing:4821239

## Is it worth to implement the foot contact switches?
One of the biggest flaws of building a quadruped robot on a budget is the fact that the actuators are not compliant. To still be able to walk on non-flat terrain, foot contact switches sense whether the leg is already supporting the body weight or not and eventually stops the legs descend. That's the theory. After fiddling around with different designs I figured out that using Force Sensing Resistors (FSR) is the best choice for building foot contact switches if one wants to maintain the original SpotMicro design and still be able to detect ground contact reliably. I connected them to an Arduino Nano and some LEDs indicating the current leg state.

After doing some tests, I saw that my control algorithm is way too slow to react to ground contact properly (50 Hz). Thus I've rewritten the core part of my code into C++. In some early tests, I got around 1000 Hz which made me really happy. After connecting the Arduino though the update rate dropped to around 100 Hz, even with an overclocked I2C connection. This means that proper ground contact control is only possible for small velocities. In my implementation, the foot contact switches are only used for a slow crawl gait and disabled for trot. This seems to be the compromise one must make with this setup. Maybe in some distant future, I will try to switch from I2C to CAN or similar or connect the Arduino and the Raspberry via GPIO.

<img src="https://github.com/ThomasSchnapka/quaro/blob/master/media/foot_contact_switches_gait.gif?raw=true" width="250">
<img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/media/foot_contact_switches_test.gif" width="250">
<img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/Hardware/Foot_contact_switch/foot_sensor_crosssection.jpg" width="250">
<img src="https://raw.githubusercontent.com/ThomasSchnapka/quaro/master/Hardware/Foot_contact_switch/foot_sensor_scheme.png" width="250">
