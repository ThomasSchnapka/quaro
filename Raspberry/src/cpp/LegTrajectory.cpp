#include <iostream>
#include "LegTrajectory.h"
#include "SingleLegTrajectory.h"
#include "COMTrajectory.h"
#include "Coordinates.h"
#include "State.h"
 
LegTrajectory::LegTrajectory(State* pstate, COMTrajectory* pcomtrajectory){
	state = pstate;
	comtrajectory = pcomtrajectory;
	
	// initialize std::vector containing legs
	leg.reserve(4);
	for(int i = 0; i<4; i++){
		leg[i] = SingleLegTrajectory(pstate, pcomtrajectory, i);
	}
}
	

LegTrajectory::~LegTrajectory() {}


Coordinates LegTrajectory::get_leg_position(float t) {
	
	Coordinates c;
	for(int i = 0; i<4; i++){
		c.col(i) = leg[i].get_leg_position(t);
	}
	
	
	return c;
}
