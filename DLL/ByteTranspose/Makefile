SRC=ByteTranspose.cpp 
HDR=ByteTranspose.h stdafx.h 
CC=g++

LIB_OUT=bin
LIB_NAME=bytetranspose

all:
	mkdir -p $(LIB_OUT)
	$(CC) -fPIC -c -o3 -std=c++17 $(SRC) -o $(LIB_OUT)/$(LIB_NAME).o 
	$(CC) -shared -o3 -std=c++17 $(LIB_OUT)/*.o -o $(LIB_OUT)/$(LIB_NAME).so 

clean:
	rm -rf $(LIB_OUT)
