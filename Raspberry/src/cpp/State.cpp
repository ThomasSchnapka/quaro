#include "State.h"

#include <iostream>
#if defined __arm__
    #include <eigen3/Eigen/Dense>
#else
    #include <Eigen/Dense>
#endif
#include "Coordinate.h"


using namespace Eigen;
 
// Default constructor
State::State() {
	support_ratio = 0.8;
	support_midpoint = 0.9;
	swing_hight = 0.01;
	cycle_time = 1.5;
	phase = Vector4f(0.0, 0.5, 0.5, 0.0);
	dx_bf << 0.01, 0.0, 0.0;
    d_rpy << 0.0, 0.0, 0.0;
	}

// Destructor
State::~State() {}

void State::set_vel_x(float vx){
	dx_bf(0) = vx;
}
void State::set_cycle_time(float ct){
	cycle_time = ct;
}
void State::set_support_ratio(float sr){
	support_ratio = sr;
}
