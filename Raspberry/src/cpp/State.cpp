#include "State.h"

#include <iostream>
#include <Eigen/Dense>


using namespace Eigen;
 
// Default constructor
State::State() {
	support_ratio = 0.8;
	support_midpoint = 0.9;
	swing_hight = 0.01;
	cycle_time = 1.5;
	//phase << 0.0 << 0.5 << 0.5 << 0.0;
	phase = Vector4f(0.0, 0.5, 0.5, 0.0);
	}

// Destructor
State::~State() {}
