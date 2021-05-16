/*
 * Interface to connect Python with C++
 */

#ifndef GAITCONTROLLER_H
#define GAITCONTROLLER_H

#include <iostream>
#include "LegTrajectory.h"
#include "BaseFrameTrajectory.h"
#include "Coordinates.h"
#include "State.h"

class GaitController {
	public:
		GaitController();
		~GaitController();
		Coordinates get_leg_position(float t);
		void set_vel_x(float vx);
		void set_cycle_time(float ct);
		void set_support_ratio(float sr);
		void set_phase(float p0, float p1, float p2, float p3);
        void set_swing_hight(float sh);
    private:
        State* state;
       	BaseFrameTrajectory* bftrajectory;
       	ContactSensor* contactsensor;
       	LegTrajectory* legtrajectory;
};


#endif