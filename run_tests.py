import _test_00_dll as dll_tests
from datetime import datetime
import sys
import json

def save_report_as_json(filename, report):
    with open(f"{filename}.json", "w") as f_report:
        json.dump(report, f_report)

def current_time_as_str():
    return datetime.now().strftime("%m-%d-%Y-%H:%M:%S")


if __name__ == "__main__":
    report = {"datetime":current_time_as_str(), "platform": f"{sys.platform}",
    "functions":{}}
    now = current_time_as_str()

    report["functions"]["TransposeWords16x16"] = dll_tests.Test_TransposeWords16x16()
    report["functions"]["TransposeWords8x8"] = dll_tests.Test_TransposeByte8x8()

    save_report_as_json(f"test_run_{now}", report)
    print(f"Results of tests on {sys.platform} run at {now}: \n{report}")
    