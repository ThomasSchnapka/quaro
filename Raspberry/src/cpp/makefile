# Makefile for Writing Make Files Example
 
# *****************************************************
# Variables to control Makefile operation
 
CC = g++
# CFLAGS = -Wall -g
CFLAGS = -g -w
INC = -I eigen-3.4-rc1 -lm
 
# *****************************************************
# linking
test: test.o GaitController.o LegTrajectory.o SingleLegTrajectory.o SwingSpline.o BaseFrameTrajectory.o State.o ContactSensor.o
	$(CC) $(CFLAGS) test.o GaitController.o LegTrajectory.o SingleLegTrajectory.o SwingSpline.o BaseFrameTrajectory.o State.o ContactSensor.o -o test
	
# *****************************************************
# compilation

test.o: test.cpp
	$(CC) $(CFLAGS) $(INC) -c test.cpp

GaitController.o: GaitController.cpp
	$(CC) $(CFLAGS) $(INC) -c GaitController.cpp
	
LegTrajectory.o: LegTrajectory.cpp
	$(CC) $(CFLAGS) $(INC) -c LegTrajectory.cpp
	
SingleLegTrajectory.o: SingleLegTrajectory.cpp
	$(CC) $(CFLAGS) $(INC) -c SingleLegTrajectory.cpp
	
SwingSpline.o: SwingSpline.cpp
	$(CC) $(CFLAGS) $(INC) -c SwingSpline.cpp

BaseFrameTrajectory.o: BaseFrameTrajectory.cpp
	$(CC) $(CFLAGS) $(INC) -c BaseFrameTrajectory.cpp
	
State.o: State.cpp
	$(CC) $(CFLAGS) $(INC) -c State.cpp
	
ContactSensor.o: ContactSensor.cpp
	$(CC) $(CFLAGS) $(INC) -c ContactSensor.cpp

clean:
	rm -r *.o
