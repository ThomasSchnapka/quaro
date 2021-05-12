#include <iostream>
#include "COMTrajectory.h"
#include "Coordinate.h"
 
// Default constructor
COMTrajectory::COMTrajectory() {
	x_com << 0, 0, 0;
	dx_com << 0.01, 0, 0;
	rpy << 0, 0, 0;
	d_rpy << 0, 0, 0;
	}

// Destructor
COMTrajectory::~COMTrajectory() {}

void COMTrajectory::update(float t){
	float dt = t - t_last;
	x_com += dt*dx_com;
	t_last = t;
}

