#include <iostream>
#include "BaseFrameTrajectory.h"
#include "Coordinate.h"
#include "State.h"
 
// Default constructor
BaseFrameTrajectory::BaseFrameTrajectory(State* pstate) {
	state = pstate;
	x_bf << 0, 0, 0;
	rpy << 0, 0, 0;
	t_last = 0;
	}

// Destructor
BaseFrameTrajectory::~BaseFrameTrajectory() {}

Coordinate BaseFrameTrajectory::predict_x_bf(float dt){
	Coordinate pos;
	pos = x_bf;
	pos += dt*state->dx_bf;
	return pos;
}

void BaseFrameTrajectory::update(float t){
	float dt = t - t_last;
	x_bf += dt*state->dx_bf;
	rpy += dt*state->d_rpy;
	t_last = t;
}

