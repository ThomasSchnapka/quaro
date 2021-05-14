#ifndef COMTRAJECTORY_H
#define COMTRAJECTORY_H

#include "Coordinate.h"
#include "State.h"

class BaseFrameTrajectory {
	public:
		BaseFrameTrajectory(State* pstate);
		~BaseFrameTrajectory();
		Coordinate x_com;
		Coordinate rpy;
		Coordinate predict_x_com(float dt);
		void update(float t);
	private:
		State* state;
		float t_last;
};


#endif
