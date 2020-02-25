from decoder import *
from types import *
from ctypes import cast, c_byte, create_string_buffer, c_ulong, POINTER
import time
import timeit
import numpy as np


class PerformanceTester:
    def __init__(self, function, name, *args, **kvargs):
        self.__tested_subject = function
        self.__tested_args = args
        self.__tested_kvargs = kvargs
        self.__avg_exec_time = 0

        self.__report_current_avg = 0
        self.__report_last_subject = name
        self.__report_last_repeats = 0
        self.__additional_info = None
    
    def meas_exec_time(self, times=1):
        
        all_exec_time = 0
        for _ in range(times):
            start = timeit.default_timer()
            self.__tested_subject(*self.__tested_args, *self.__tested_kvargs)
            stop = timeit.default_timer()
            
            all_exec_time += (stop-start)
        
        self.__report_current_avg = all_exec_time/times
        self.__report_last_repeats = times
    
    def add_to_report(self, kv_info):
        self.__additional_info = kv_info
    
    def get_report(self):
        report = {}
        report["avg_time"] = self.__report_current_avg
        report["repeats"] = self.__report_last_repeats

        if self.__additional_info is not None:
            for k,v in self.__additional_info.items():
                report[k] = v

        return report


def bytes_number_to_str(number):

    ret_str = ""

    if number < 1024:
        ret_str = f"{number} B"
    elif (number >= 1024) and (number < 1024**2):
        ret_str = f"{round(number/1024, 2)} KB"
    elif (number >= 1024**2) and (number < 1024**3):
        ret_str = f"{round(number/1024**2, 2)} MB"
    elif (number >= 1024**3) and (number < 1024**4):
        ret_str = f"{round(number/1024**3, 2)} GB"

    return ret_str


def Test_Deinterleve_16Bytes_to_2x8Bytes_bytestream(size=(1024**3)):

    data_in = np.ctypeslib.as_ctypes(np.random.randint(low=0, high=2**7-1, \
                dtype=np.int8, size=size)) 

    performanceTester = PerformanceTester(Deinterleve_16Bytes_to_2x8Bytes, \
                                        "Deinterleve_16Bytes_to_2x8Bytes",\
                                        data_in, size//16)
    performanceTester.meas_exec_time()
    performanceTester.add_to_report({"buffer_size": bytes_number_to_str(size)})

    return performanceTester.get_report()


def Test_TransposeByte8x8():

    a = [   0b00000001, 
            0b10000001, 
            0b00000001, 
            0b10000000, 
            0b00000000, 
            0b00000000, 
            0b00000000, 
            0b00000000,
           ]

    arr = (BYTE * len(a))(*a)
    brr = (BYTE * len(a))(*a)

    performanceTester = PerformanceTester(TransposeByte8x8, "TransposeByte8x8", arr, brr)
    performanceTester.meas_exec_time(10000)

    return performanceTester.get_report()
        

def Test_TransposeBits_16xI8_to_8xI16_bytestream(bytestream_size=1024**3):

    data_in = np.ctypeslib.as_ctypes(np.random.randint(low=0, high=2**7-1, \
                dtype=np.int8, size=bytestream_size)) 

    performanceTester = PerformanceTester(TransposeBits_16xI8_to_8xI16, "TransposeBits_16xI8_to_8xI16",\
                                            data_in, len(data_in)//16)

    performanceTester.meas_exec_time()
    performanceTester.add_to_report({"buffer_size": bytes_number_to_str(bytestream_size)})

    return performanceTester.get_report()


def Test_Deinterleve_14x8Words_to_8x14Words_bytestream(bytestream_size=(1024**2)*14*8):

    data_in = np.ctypeslib.as_ctypes(np.random.randint(low=0, high=2**7-1, \
                dtype=np.uint16, size=bytestream_size)) 
    
    Deinterleve_14x8Words_to_8x14Words(data_in, bytestream_size//(14*8))
    performanceTester = PerformanceTester(Deinterleve_14x8Words_to_8x14Words, \
                        "Deinterleve_14x8Words_to_8x14Words",\
                        data_in, bytestream_size//(14*8))

    performanceTester.meas_exec_time()
    performanceTester.add_to_report({"buffer_size": bytes_number_to_str(bytestream_size)})

    return performanceTester.get_report()

def Test_TransposeBits_14xI16_to_16xI16_bytestream(bytestream_size=1024**3):

    chunks_nr = bytestream_size//14
    data_in = np.ctypeslib.as_ctypes(np.random.randint(low=0, high=2**16-1, \
                dtype=np.uint16, size=bytestream_size))    
    data_out = (WORD*(chunks_nr*16))()

    performanceTester = PerformanceTester(TransposeBits_14xI16_to_16xI16, "TransposeBits_14xI16_to_16xI16",\
        data_in, data_out, chunks_nr) 
    performanceTester.meas_exec_time()
    performanceTester.add_to_report({"buffer_size": bytes_number_to_str(bytestream_size)})
    
    return performanceTester.get_report()
    
def Test_TransposeWords16x16():

    a = [   0b0000000111001010, 
            0b1000000100000001, 
            0b0000000101010101, 
            0b1000000011001101, 
            0b0000000000001100, 
            0b0000000000000000, 
            0b0000000000000000, 
            0b0000000000000000,
            0b1111111111111111,
            0b1111111100000000,
            0b0011001100110011,
            0b0000000000000000,
            0b0000000000000000,
            0b1111111111111111,
            0b1011100011101010,
            0b0000000000000000,
           ]

    arr = (WORD * len(a))(*a)
    brr = (WORD * len(a))(*a)

    performanceTester = PerformanceTester(TransposeWords16x16, "TransposeWords16x16",arr, brr)
    performanceTester.meas_exec_time(10000)
    
    return performanceTester.get_report()

def Test_decode_chip_byte_stream_to_pixel_array(bytestream_size=1146880000):

    bytestream = (BYTE*bytestream_size)()
    GenerateRandomBytestream(bytestream, DWORD(bytestream_size), DWORD(np.random.randint(timeit.default_timer())))

    performanceTester = PerformanceTester(decode_chip_byte_stream_to_pixel_array, \
        "decode_chip_byte_stream_to_pixel_array", bytestream)
    performanceTester.meas_exec_time(1)
    performanceTester.add_to_report({"buffer_size": bytes_number_to_str(bytestream_size)})

    return performanceTester.get_report()
