import _test_00_dll as dll_tests
from datetime import datetime
import sys
import json
from cpuinfo import get_cpu_info

def save_report_as_json(filename, report):
    with open(f"{filename}.json", "w") as f_report:
        json.dump(report, f_report)

def current_time_as_str():
    return datetime.now().strftime("%m-%d-%Y-%H-%M-%S")


if __name__ == "__main__":
    report = {"datetime":current_time_as_str(), "platform": f"{sys.platform}",
    "functions":{}, "cpu":get_cpu_info()["brand"]}
    now = current_time_as_str()
    report_dir = "Results"

    report["functions"]["TransposeWords16x16"] = dll_tests.Test_TransposeWords16x16()
    report["functions"]["TransposeWords8x8"] = dll_tests.Test_TransposeByte8x8()
    report["functions"]["decode_chip_byte_stream_to_pixel_array"] = dll_tests.Test_decode_chip_byte_stream_to_pixel_array()
    report["description"] =  "" # insert here additional description of test

    save_report_as_json(f"Results/test_run_{now}", report)
    print(f"Results of tests on {sys.platform} run at {now}: \n{report}")
    
