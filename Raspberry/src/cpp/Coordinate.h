/*
 * Definition of a 3x1 matrix used to describe a single leg coordinates
 * 
 * Columns differentiate legs, rows differentiate single coodinates
 * 
 * 		x
 * 		y
 * 		z
 * 
 */

#ifndef COORDINATE_H
#define COORDINATE_H

#include <iostream>
#if defined __arm__
    #include <eigen3/Eigen/Dense>
#else
    #include <Eigen/Dense>
#endif

using namespace Eigen;

class Coordinate : public Matrix<float, 3, 1> {
	public:
		Coordinate() : Matrix<float, 3, 1>(){}
};


#endif
