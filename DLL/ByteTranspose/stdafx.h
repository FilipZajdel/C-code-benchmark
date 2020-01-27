// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once

#if defined(_WIN32) || defined(_WIN64)
#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers
// Windows Header Files:
#include "targetver.h"
#include <windows.h>
#elif defined(__linux)
#undef BYTE_TRANSPOSE_API
#define BYTE_TRANSPOSE_API 
#define WINAPI 
typedef unsigned char BYTE;
typedef unsigned long DWORD;
typedef unsigned short WORD;
#endif



// TODO: reference additional headers your program requires here
