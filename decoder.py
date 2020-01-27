from types_wrapper import *
import numpy as np
from ctypes import cast, POINTER

void = None
#dll = C_DLL(r"DLL/ByteTranspose/bin/bytetranspose.so")
dll = C_DLL(r"C:\\Users\\Filip\\Downloads\\DLL_V2\\DLL\\DLL\\x64\\Release\\ByteTranspose.dll")

# void WINAPI TransposeByte8x8(BYTE * source, BYTE * dest,)
prototype = C_FUNCTYPE(void, POINTER(BYTE),POINTER(BYTE))
TransposeByte8x8 = prototype(("TransposeByte8x8", dll))

# void WINAPI TransposeWords16x16(WORD * source, WORD * dest,)
prototype = C_FUNCTYPE(void, POINTER(WORD),POINTER(WORD))
TransposeWords16x16 = prototype(("TransposeWords16x16", dll))

#void WINAPI TransposeBits_16xI8_to_8xI16(BYTE * bSource, DWORD count)
prototype = C_FUNCTYPE(void, POINTER(BYTE), DWORD)
TransposeBits_16xI8_to_8xI16 = prototype(("TransposeBits_16xI8_to_8xI16", dll))

# void WINAPI Deinterleve_16Bytes_to_2x8Bytes(BYTE* pbSource, DWORD count);
prototype = C_FUNCTYPE(void, POINTER(BYTE), DWORD)
Deinterleve_16Bytes_to_2x8Bytes = prototype(("Deinterleve_16Bytes_to_2x8Bytes", dll))

# void WINAPI Deinterleve_14x8Words_to_8x14Words(BYTE* pbSource, DWORD count);
# a0,a1,..,a13; b0,b1,..,b13; ..;z0,z1,..z13
# a0,b0,..,z0; a1,b1,..,z1; ..; a13,b13,..,z13
prototype = C_FUNCTYPE(void, POINTER(WORD), DWORD)
Deinterleve_14x8Words_to_8x14Words = prototype(("Deinterleve_14x8Words_to_8x14Words", dll))

# void WINAPI TransposeBits_14xI16_to_16xI16(WORD* source, WORD* destination, DWORD chunks)
prototype = C_FUNCTYPE(void, POINTER(WORD),POINTER(WORD),DWORD)
TransposeBits_14xI16_to_16xI16 = prototype(("TransposeBits_14xI16_to_16xI16", dll))

def decode_chip_byte_stream_to_pixel_array(byte_stream): 
    len_byte_stream = len(byte_stream)            
    Deinterleve_16Bytes_to_2x8Bytes(byte_stream,len_byte_stream//16)    
    TransposeBits_16xI8_to_8xI16(byte_stream,len_byte_stream//16)        
    byte_stream = cast(byte_stream, POINTER(WORD))      
    Deinterleve_14x8Words_to_8x14Words(byte_stream,len_byte_stream//(14*8*2))    

    ctrs = (WORD * ((len_byte_stream*16)//14//2))()     
    TransposeBits_14xI16_to_16xI16(byte_stream,ctrs,len(ctrs)//16)    
    
    ctrs = np.ctypeslib.as_array(ctrs)    
    return ctrs.reshape((len(ctrs)//(2*256*128),2,256,128)) # frame,ctr,column,row    

