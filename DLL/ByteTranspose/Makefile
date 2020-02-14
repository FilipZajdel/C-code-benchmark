SRC=ByteTranspose.cpp 
HDR=ByteTranspose.h stdafx.h 
CC=gcc

LIB_OUT=bin
LIB_NAME=bytetranspose

all:
	mkdir -p $(LIB_OUT)
	$(CC) -fPIC -c -o3 $(SRC) -o $(LIB_OUT)/$(LIB_NAME).o
	$(CC) -shared $(LIB_OUT)/*.o -o $(LIB_OUT)/$(LIB_NAME).so

clean:
	rm -rf $(LIB_OUT)
