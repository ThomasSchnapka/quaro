#ifndef STATE_H
#define STATE_H

#include <iostream>
#include <Eigen/Dense>
#include "Coordinate.h"

using namespace Eigen;

class State {
	public:
		State();
		~State();
		float support_ratio;
		float support_midpoint;
		float swing_hight;
		int cycle_time;
		Vector4f phase;
		
		Coordinate dx_bf;
		Coordinate d_rpy;
		
		void set_vel_x(float vx);
		void set_cycle_time(float ct);
		void set_support_ratio(float sr);
		
		
};


#endif
