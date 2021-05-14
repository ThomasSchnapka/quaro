#include <iostream>
#include "LegTrajectory.h"
#include "SingleLegTrajectory.h"
#include "BaseFrameTrajectory.h"
#include "Coordinates.h"
#include "State.h"


LegTrajectory::LegTrajectory(State* pstate, BaseFrameTrajectory* pbftrajectory){
	state = pstate;
	bftrajectory = pbftrajectory;
	
	// initialize std::vector containing legs
	leg.reserve(4);
	for(int i = 0; i<4; i++){
		leg[i] = SingleLegTrajectory(pstate, pbftrajectory, i);
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

std::vector<bool> LegTrajectory::int_to_bool(int p){
	// transforms the data from foot contact switches into bool vector
    std::vector<bool> c;
    c.reserve(4);
    c[0] = (    p/8 == 1);
    c[1] = ((p%8)/4 == 1);
    c[2] = ((p%4)/2 == 1);
    c[3] = ((p%2)   == 1);
    return c;
}
