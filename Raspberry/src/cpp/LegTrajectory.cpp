/*
 * Contains and collects data from single leg trajectories 
 */

#include <iostream>
#include "LegTrajectory.h"
#include "SingleLegTrajectory.h"
#include "BaseFrameTrajectory.h"
#include "Coordinates.h"
#include "State.h"
#include "ContactSensor.h"


LegTrajectory::LegTrajectory(State* pstate, BaseFrameTrajectory* pbftrajectory){
	state = pstate;
	bftrajectory = pbftrajectory;
	contactsensor = new ContactSensor();
	
	// initialize std::vector containing legs
	leg.reserve(4);
	for(int i = 0; i<4; i++){
		leg[i] = SingleLegTrajectory(pstate, pbftrajectory, i);
	}
	
}
	

LegTrajectory::~LegTrajectory() {}


Coordinates LegTrajectory::get_leg_position(float t) {
    // update BaseFrame position
    bftrajectory->update(t);
    
    // get ContactSensor readings and update leg positions
    std::vector<bool> csr = contact_sensor_result();
	Coordinates c;
	for(int i = 0; i<4; i++){
		c.col(i) = leg[i].get_leg_position(t, csr[i]);
	}
	return c;
}

std::vector<bool> LegTrajectory::contact_sensor_result(){
	/*
	 * reads data from contact sensor and converts it into a bool vector
	 */
    int p = contactsensor->read_contact_sensor();
    std::vector<bool> c;
    c.reserve(4);
    c[3] = (    p/8 == 1);
    c[2] = ((p%8)/4 == 1);
    c[1] = ((p%4)/2 == 1);
    c[0] = ((p%2)   == 1);
    return c;
}
