C_DLL = None
C_FUNCTYPE = None
BYTE = None
WORD = None
DWORD = None

import sys
if "linux" in sys.platform:
    from ctypes import CDLL 
    from ctypes import CFUNCTYPE 
    from ctypes import c_byte 
    from ctypes import c_ushort 
    from ctypes import c_ulong
    C_DLL = CDLL
    C_FUNCTYPE = CFUNCTYPE
    BYTE = c_byte
    WORD = c_ushort
    DWORD = c_ulong

elif "win" in sys.platform:
    from ctypes import WinDLL
    from ctypes import WINFUNCTYPE 
    from ctypes.wintypes import BYTE as _BYTE 
    from ctypes.wintypes import WORD as _WORD
    from ctypes.wintypes import DWORD as _DWORD
    C_DLL = WinDLL
    C_FUNCTYPE = WINFUNCTYPE
    BYTE = _BYTE
    WORD = _WORD
    DWORD = _DWORD
