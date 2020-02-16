
#ifndef BYTE_TRANSPOSE_H
#define BYTE_TRANSPOSE_H

#if defined(_WIN64) || defined(_WIN32)
#ifdef BYTE_TRANSPOSE_EXPORTS
#define BYTE_TRANSPOSE_API     __declspec(dllexport)
#else
#define BYTE_TRANSPOSE_API     __declspec(dllimport)
#pragma comment (lib, "ByteTranspose.lib")
#endif // BYTE_TRANSPOSE_EXPORTS
#endif // defined(_WIN64) || defined(_WIN32)


#ifdef __cplusplus 
extern "C" {
#endif // __cplusplus
#include "stdafx.h"
   
    BYTE_TRANSPOSE_API  void WINAPI Deinterleve_16Bytes_to_2x8Bytes(BYTE* pbSource, DWORD count);

    BYTE_TRANSPOSE_API  void WINAPI TransposeByte8x8 (BYTE* source, BYTE* destination);

    BYTE_TRANSPOSE_API  void WINAPI TransposeWords16x16 (WORD* source, WORD* destination);

    BYTE_TRANSPOSE_API  void WINAPI TransposeBits_16xI8_to_8xI16(BYTE* bSource,  DWORD count);
    
    BYTE_TRANSPOSE_API  void WINAPI Deinterleve_14x8Words_to_8x14Words(WORD* pbSource, DWORD count);

    BYTE_TRANSPOSE_API  void WINAPI TransposeBits_14xI16_to_16xI16(WORD* source, WORD* destination, DWORD chunks);

    BYTE_TRANSPOSE_API  void WINAPI GenerateRandomBytestream(BYTE* destination, DWORD size, DWORD seed);

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // BYTE_TRANSPOSE_H
