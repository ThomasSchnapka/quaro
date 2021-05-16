/*
 * Interface to connect Python with C++
 */

#include <iostream>
#include "GaitController.h"
#include "LegTrajectory.h"
#include "BaseFrameTrajectory.h"
#include "Coordinates.h"
#include "State.h"


GaitController::GaitController(){
	state = new State();
	contactsensor = new ContactSensor();
	bftrajectory = new BaseFrameTrajectory(state);
	legtrajectory = new LegTrajectory(state, bftrajectory);
}
	

GaitController::~GaitController() {}


Coordinates GaitController::get_leg_position(float t) {
	Coordinates c;
	c = legtrajectory->get_leg_position(t);
	return c;
}


void GaitController::set_vel_x(float vx){
	state->dx_bf(0) = vx;
}

void GaitController::set_cycle_time(float ct){
	state->cycle_time = ct;
}

void GaitController::set_support_ratio(float sr){
	state->support_ratio = sr;
	state->support_midpoint = sr + 0.5*(1.0-sr);
}

void GaitController::set_phase(float p0, float p1, float p2, float p3){
	state->phase(0) = p0;
	state->phase(1) = p1;
	state->phase(2) = p2;
	state->phase(3) = p3;
}

void GaitController::set_swing_hight(float sh){
	state->swing_hight = sh;
}
