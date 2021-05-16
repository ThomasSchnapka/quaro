/*
 * Generates splines for swing phase
 */

#ifndef SWINGSPLINE_H
#define SWINGSPLINE_H

#include <iostream>
#if defined __arm__
    #include <eigen3/Eigen/Dense>
#else
    #include <Eigen/Dense>
#endif
#include "Coordinate.h"
#include "State.h"
#include "BaseFrameTrajectory.h"

class SwingSpline {
	public:
		SwingSpline(State* pstate, BaseFrameTrajectory* pbftrajectory);
		~SwingSpline();
		Coordinate get_leg_position(float tn); 
		void update_spline(Coordinate pliftoff_pos);
	private:
	State* state;
	BaseFrameTrajectory* bftrajectory;
	Coordinate liftoff_pos;
	Coordinate touchdown_pos;
	Vector4f calc_coefficients(float x0, float dx0, float x1, float dx1,float T);
	float eval_spline(Vector4f a, float t);
	Vector4f ax;
	Vector4f ay;
	Vector4f az1;
	Vector4f az2;
	
};


#endif
