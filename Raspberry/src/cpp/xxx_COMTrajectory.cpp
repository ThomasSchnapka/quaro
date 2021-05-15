#include <iostream>
#include "COMTrajectory.h"
#include "Coordinate.h"
#include "State.h"
 
// Default constructor
COMTrajectory::COMTrajectory(State* pstate) {
	state = pstate;
	x_com << 0, 0, 0;
	rpy << 0, 0, 0;
	t_last = 0;
	}

// Destructor
COMTrajectory::~COMTrajectory() {}

Coordinate COMTrajectory::predict_x_com(float dt){
	Coordinate pos;
	pos = x_com;
	pos += dt*state->dx_com;
	return pos;
}

void COMTrajectory::update(float t){
	float dt = t - t_last;
	x_com += dt*state->dx_com;
	rpy += dt*state->d_rpy;
	t_last = t;
}

