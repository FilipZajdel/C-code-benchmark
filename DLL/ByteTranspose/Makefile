SRC=ByteTranspose.cpp 
HDR=ByteTranspose.h stdafx.h 
CC=g++
CC_OPTS=-g -o3

LIB_OUT=bin
LIB_NAME=bytetranspose

all:
	mkdir -p $(LIB_OUT)
	$(CC) -fPIC -c $(CC_OPTS) -std=c++17 $(SRC) -o $(LIB_OUT)/$(LIB_NAME).o 
	$(CC) -shared $(CC_OPTS) -std=c++17 $(LIB_OUT)/*.o -o $(LIB_OUT)/$(LIB_NAME).so 

clean:
	rm -rf $(LIB_OUT)
