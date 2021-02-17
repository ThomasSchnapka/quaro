# Visualisation for Quaro Quadruped Robot v4

With this collection of scripts, it is possible to visualise the robot's movement in a diagram. This can be done in operation as well as standalone to verify new parameters or algorithms.

![gif](https://github.com/ThomasSchnapka/quaro/blob/v4/Simulation/anim.gif)

(sorry for this sloppy gif, my laptop has the computing power of a potato. The live visualisation is way smoother)

## How it works

`PlotDataClient` connects with a server running on the robot (and on my computer as well) and retrieves all data needed for visualisation. 
This data is then processed by `QuaroPlot3D` to display the state of the robots legs as well as body. The joint positions are calculated by 
`forward_kinematics` using these definitions:

![definitions](https://github.com/ThomasSchnapka/quaro/blob/v4/Simulation/Quaro_Kinematics.png)

## Next steps
- [ ] display support triangle and stability margin
- [ ] display torque for every joint
- [ ] make this whole animation faster, maybe by changing from Matplotlib to Pygame or Tkinter
- [ ] display leg trajectory
