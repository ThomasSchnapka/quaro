/*
 * Generates and calculates splines for swing phase
 * 
 * movement in x an y direction consist of one cubic spline, movement
 * in z direction consits of two cubic splines.
 * 
 */


#include <iostream>
#include <Eigen/Dense>
#include "SwingSpline.h"
#include "Coordinate.h"
#include "State.h"
#include "COMTrajectory.h"

 
// Default constructor
SwingSpline::SwingSpline(State* pstate, COMTrajectory* pcomtrajectory) {
	state = pstate;
	comtrajectory = pcomtrajectory;
	Coordinate c;
	c << 0.0, 0.0, 0.0;
	update_spline(c);
	}

// Destructor
SwingSpline::~SwingSpline() {}


Coordinate SwingSpline::get_leg_position(float tn) {
	Coordinate m;
	m(0) = eval_spline(ax, tn - state->support_ratio);
	m(1) = eval_spline(ay, tn - state->support_ratio);
	if(tn < state->support_midpoint){
		m(2) = eval_spline(az1, tn - state->support_ratio);
	}else{
		m(2) = eval_spline(az2, tn - state->support_midpoint);
	}
	return m;
}

void SwingSpline::update_spline(Coordinate pliftoff_pos){
	liftoff_pos = pliftoff_pos;
	touchdown_pos = comtrajectory->predict_x_com();
	touchdown_pos *= 0.5;
	
	// calculate new spline coefficients
	// TODO: add derivatives
	float T = 1.0 - state->support_ratio;
	float Tm = 1.0 - state->support_midpoint;
	ax =  calc_coefficients(liftoff_pos(0),     0, touchdown_pos(0),   0, T);
	ay =  calc_coefficients(liftoff_pos(1),     0, touchdown_pos(1),   0, T);
	az1 = calc_coefficients(liftoff_pos(2),     0, state->swing_hight, 0, Tm);
	az2 = calc_coefficients(state->swing_hight, 0, touchdown_pos(2),   0, (T-Tm));
	
}

Vector4f SwingSpline::calc_coefficients(float x0, float dx0, float x1, 
										float dx1,float T){
	// Spline coefficients taken from A.Winklers PhD Thesis
	// https://storage.googleapis.com/concise-hue-230505.appspot.com/pdfs/18-phd-winkler.pdf
	// p.86
	Vector4f a;
	a(0) = x0;
	a(1) = dx0;
	a(2) = -(3*(x0-x1) + T*(2*dx0 + dx1))/(T*T);
	a(3) = (2*(x0-x1) + T*(dx0 + dx1))/(T*T*T);
	return a;
}

float SwingSpline::eval_spline(Vector4f a, float t){
	return a(0) + a(1)*t + a(2)*t*t + a(3)*t*t*t; 
}


