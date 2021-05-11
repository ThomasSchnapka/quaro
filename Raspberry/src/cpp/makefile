# Makefile for Writing Make Files Example
 
# *****************************************************
# Variables to control Makefile operation
 
CC = g++
CFLAGS = -Wall -g
INC = -I eigen-3.4-rc1
 
# ****************************************************
# Targets needed to bring the executable up to date

test: test.o SwingSpline.o
	$(CC) $(CFLAGS) test.o SwingSpline.o -o test

test.o: test.cpp
	$(CC) $(CFLAGS) $(INC) -c test.cpp

SwingSpline.o: SwingSpline.cpp
	$(CC) $(CFLAGS) -c SwingSpline.cpp

clean:
	rm -r *.o
