/*
 * Definition of a 3x4 matrix used to describe leg coordinates. This
 * is the defintion used to convert Eigen matrices into Numpy arrays
 * 
 * Columns differentiate legs, rows differentiate single coodinates
 * 
 * 		x0	x1	x2	x3
 * 		y0	y1	y2	y3
 * 		z0	z1	z2	z3
 * 
 */

#ifndef COORDINATES_H
#define COORDINATES_H

#include <Eigen/Dense>

using namespace Eigen;

class Coordinates : public Matrix<float, 3, 4> {
	public:
		Coordinates() : Matrix<float, 3, 4>(){}
};


#endif
