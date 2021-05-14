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
		
		Coordinate dx_com;
		Coordinate d_rpy;
		
		
};


#endif
