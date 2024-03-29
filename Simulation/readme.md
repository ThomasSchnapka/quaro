# Visualisation for Quaro Quadruped Robot v4

With this collection of scripts, it is possible to visualise the robot's movement in a diagram. This can be done in operation as well as standalone to verify new parameters or algorithms.

![gif](https://github.com/ThomasSchnapka/quaro/blob/v4/Simulation/doc/anim.gif)

(sorry for this sloppy gif, my laptop has the computing power of a potato. The live visualisation is way smoother)

## How it works

`PlotDataClient` connects with a server running on the robot (and on my computer as well) and retrieves all data needed for visualisation. 
This data is then processed by `QuaroPlot3D` to display the state of the robots legs as well as body. The joint positions are calculated by 
`forward_kinematics` using these definitions:

![definitions](https://github.com/ThomasSchnapka/quaro/blob/v4/Simulation/doc/Quaro_Kinematics.png)

## Next steps
- [x] display support triangle
- [ ] display stability margin
- [ ] display torque for every joint
- [x] make this whole animation faster
- [ ] display leg trajectory
