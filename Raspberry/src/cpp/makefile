# Makefile for Writing Make Files Example
 
# *****************************************************
# Variables to control Makefile operation
 
CC = g++
# CFLAGS = -Wall -g
CFLAGS = -g -w
INC = -I eigen-3.4-rc1
 
# *****************************************************
# linking
test: test.o LegTrajectory.o SingleLegTrajectory.o SwingSpline.o COMTrajectory.o State.o
	$(CC) $(CFLAGS) test.o LegTrajectory.o SingleLegTrajectory.o SwingSpline.o COMTrajectory.o State.o -o test
	
# *****************************************************
# compilation

test.o: test.cpp
	$(CC) $(CFLAGS) $(INC) -c test.cpp
	
LegTrajectory.o: LegTrajectory.cpp
	$(CC) $(CFLAGS) $(INC) -c LegTrajectory.cpp
	
SingleLegTrajectory.o: SingleLegTrajectory.cpp
	$(CC) $(CFLAGS) $(INC) -c SingleLegTrajectory.cpp
	
SwingSpline.o: SwingSpline.cpp
	$(CC) $(CFLAGS) $(INC) -c SwingSpline.cpp

COMTrajectory.o: COMTrajectory.cpp
	$(CC) $(CFLAGS) $(INC) -c COMTrajectory.cpp
	
State.o: State.cpp
	$(CC) $(CFLAGS) $(INC) -c State.cpp

clean:
	rm -r *.o
