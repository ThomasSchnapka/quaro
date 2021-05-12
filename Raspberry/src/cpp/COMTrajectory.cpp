#include <iostream>
#include "COMTrajectory.h"
#include "Coordinate.h"
#include "State.h"
 
// Default constructor
COMTrajectory::COMTrajectory(State* pstate) {
	state = pstate;
	x_com << 0, 0, 0;
	dx_com << 0.01, 0, 0;
	rpy << 0, 0, 0;
	d_rpy << 0, 0, 0;
	}

// Destructor
COMTrajectory::~COMTrajectory() {}

Coordinate COMTrajectory::predict_x_com(){
	float dt = (1.0 - state->support_ratio)*state->cycle_time;
	Coordinate pos = x_com;
	pos += dt*dx_com;
	return pos;
}

void COMTrajectory::update(float t){
	float dt = t - t_last;
	x_com += dt*dx_com;
	rpy += dt*d_rpy;
	t_last = t;
}

