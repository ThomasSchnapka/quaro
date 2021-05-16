/*
 *  State containing shared information between modules
 */

#ifndef STATE_H
#define STATE_H

#include <iostream>
#if defined __arm__
    #include <eigen3/Eigen/Dense>
#else
    #include <Eigen/Dense>
#endif
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
		
		EIGEN_MAKE_ALIGNED_OPERATOR_NEW
		Coordinate dx_bf;
		Coordinate d_rpy;		
		
};


#endif
