# C functions performance tests across different devices

**Table of contents:**
* [Website](https://filipzajdel.github.io/C-code-benchmark/)
* [Goals](#goals)
* [Repository structure](#repository-structure)
* [Building on Windows](#building-on-windows)
* [Building on Linux](#building-on-linux)
* [Running tests](#running-tests)
* [Results](#results)

#

## Goals

1. VS2019 project and Makefile based project ready to be compiled using the same source code.
2. Python wrappers for C functions and for profiling.
3. Running tests on Windows and Linux installed on the same PC and Linux installed on Raspberry Pi 4. 
4. Parser for files created during test execution with test results.

## Repository Structure

><br>- DLL *(Contains C Code)*
><br>- Results *(Test results are saved here)*
><br>- docs *(contains website files)*
><br>- functional_tests.py 
><br>- generate_html_report.py *(Generates HTML file filled with results)*
><br>- README.md 
><br>- run_tests.py *(Starts tests execution)*
><br>- timing_tests.py *(Contains definitons of tests)*
><br>- types_wrapper.py *(Provides common api of CTypes for Linux and Windows)*
><br>- decoder.py *(Provides api for imported library)*

## Building on Windows

Requirements:

* Visual Studio 2019 

Steps:

* Go to DLL directory, open ByteTranspose.sln and build it using VS2019
* Check where dll is put after build and save path
* Open decoder.py and change dll_path to absolute path where dll is saved
* Go to section [Running tests](#running-tests)

## Building on Linux

Requirements:
* gcc
* make

Steps:
* Open terminal

``` sh
    $ cd C_functions_timing_tests/DLL/ByteTranspose
    $ make -j4
```
* Open decoder.py and change dll_path to r"DLL/ByteTranspose/bin/bytetranspose.so"
* Go to section [Running tests](#running-tests)

## Running tests

Requirements:
* Python >= 3.6.9 
* pip3

Setup:
``` sh
    $ sudo pip3 install -r requirements.txt
```

Steps:
* run script run_tests.py (Execution of tests takes some time, depending on number of functions tested and test vector size)
* results are saved in *Results* directory

Each execution of "run_tests.py" produces *.json file named after time of test execution using following format:

```json
{
    "datetime": "string",
    "platform": "string",
    "functions": {
        "string": {
            "avg_time": double,
            "repeats": integer,
            "buffer_size": "string"
        },
        "string": {
            "avg_time": double,
            "repeats": integer,
            "buffer_size": "string"
        },
        "string": {
            "avg_time": double,
            "repeats": integer,
            "buffer_size": "string"
        }
    },
    "cpu": "string",
    "description": "string",
    "compiler": "string",
    "compiler-opt": "string",
    "compiler-opt-desc": "string"
}
```

## Results

Results of tests already executed on PC and Raspberry Pi are presented [here](https://filipzajdel.github.io/C_functions_timing_tests/)

