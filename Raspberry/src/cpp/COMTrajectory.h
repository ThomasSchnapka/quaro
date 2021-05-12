#ifndef COMTRAJECTORY_H
#define COMTRAJECTORY_H

#include "Coordinate.h"

class COMTrajectory {
	public:
		COMTrajectory();
		~COMTrajectory();
		Coordinate x_com;
		Coordinate dx_com;
		Coordinate rpy;
		Coordinate d_rpy;
		void update(float t);
	private:
		float t_last;
};


#endif
