# ByteTranspose Performace Test

Project contains set of tests that are going to be executed on different platform and machines in order to compare their 
performance.

**Table of contents:**
* [Goals](#goals)
* [Results](#results)

## Goals

1. VS2019 project and Makefile based project ready to be compiled using the same source code.
2. Python wrappers for C functions and for profiling.
3. Running tests on Windows and Linux installed on the same PC and Linux installed on Raspberry Pi 4. 

## Results

Results are collected in directory [Results](https://github.com/FilipZajdel/ByteTranspose/tree/master/Results) 


After execution of tests, results are written to json file in specified format:

```json
{
    "datetime":"",
    "platform":"",
    "functions":{
        "dummy_name":{
            "avg_time": Double
        },
        "dummt_name2":{
            "avg_time": Double
        }
    }
}
```
