import timing_tests
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

    report["functions"]["TransposeWords16x16"] = timing_tests.Test_TransposeWords16x16()
    report["functions"]["TransposeWords8x8"] = timing_tests.Test_TransposeByte8x8()
    report["functions"]["decode_chip_byte_stream_to_pixel_array"] = timing_tests.Test_decode_chip_byte_stream_to_pixel_array()

    report["functions"]["Deinterleve_16Bytes_to_2x8Bytes"] = timing_tests.Test_Deinterleve_16Bytes_to_2x8Bytes_bytestream()
    report["functions"]["TransposeBits_16xI8_to_8xI16"] = timing_tests.Test_TransposeBits_16xI8_to_8xI16_bytestream()
    report["functions"]["Deinterleve_14x8Words_to_8x14Word"] = timing_tests.Test_Deinterleve_14x8Words_to_8x14Words_bytestream()
    report["functions"]["TransposeBits_14xI16_to_16xI16"] = timing_tests.Test_TransposeBits_14xI16_to_16xI16_bytestream()

    report["description"] =  "" # insert here additional description of test if required
    report["compiler"] = "gcc 7.4"

    save_report_as_json(f"Results/test_run_{now}", report)
    print(f"Results of tests on {sys.platform} run at {now}: \n{report}")
    
