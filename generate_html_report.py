from yattag import Doc
import os
import json

doc, tag, text = Doc().tagtext()

RESULTS_DIRECTORY = "Results"
FUNCTION_DEFS_FILE = "function_defs.json"

class ReportReader:
    def __init__(self, report_dir, function_defs_file):
        self.reports = self.__load_json_reports(report_dir)
        function_defs = self.__load_function_defs(function_defs_file)

        self.__functions = self.__prepare_functions_info(function_defs)
    
    def __load_json_reports(self, directory):
        files = [d for d in os.listdir(directory) if ".json" in d]
        merged_report = {}

        for report in files:
            with open(f"{directory}/{report}", "r") as fp:
                merged_report[report] = json.load(fp)

        return merged_report
    
    def __load_function_defs(self, def_file):
        with open(def_file, "r") as func_defs:
            return json.load(func_defs) 

    def __prepare_functions_info(self, function_defs):
        functions = []
        function_data_struct = {"name":None, "body":None, "details":None, "vector_sizes":[], "timings":[]}
        timings_data_struct = {"device":None, "platform":None, "times":{}}

        # Extract function names
        func_names = sum([[f for f in report.get("functions").keys()] for report in self.reports.values()],[])
        func_names = list(dict.fromkeys(func_names))

        # Extract cpu and os pairs
        dev_os_pairs = [(report.get("cpu"), report.get("platform")) for report in self.reports.values()]
        dev_os_pairs = list(dict.fromkeys(dev_os_pairs))

        # Extract buffer sizes of functions
        buffer_sizes = dict.fromkeys(func_names, [])
        for report in self.reports.values():
            for func_name, data in report.get("functions").items():
                buffer_sizes[func_name].append(data["buffer_size"])
        buffer_sizes = {func_name:list(dict.fromkeys(sizes)) for (func_name,sizes) in buffer_sizes.items()}

        for func_name in func_names:
            func_info = {**function_data_struct}
            func_info["name"] = func_name
            func_info["body"] = function_defs.get(func_name, {}).get("body", "")
            func_info["details"] = function_defs.get(func_name, {}).get("details", "")

            timing_infos = []
            vector_sizes = []
            for dev, os in dev_os_pairs:
                timing_info = {}
                timing_info["device"] = dev
                timing_info["platform"] = os
                timing_info["times"] = {}

                for report in self.reports.values():
                    if dev == report["cpu"] and os == report["platform"]:
                        if func_name in report.get("functions"):
                            vector_size = report.get("functions")[func_name]["buffer_size"]
                            vector_sizes.append(vector_size)
                            avg_time = report.get("functions")[func_name]["avg_time"]

                            timing_info["times"][vector_size] = avg_time

                timing_infos.append(timing_info)

            func_info["vector_sizes"] = list(dict.fromkeys(vector_sizes))
            func_info["timings"] = [t for t in timing_infos]
            functions.append(func_info)

        return functions

    def get_functions(self, sort_by="buffer_size"): 
        return self.__functions

def cpu_to_device(cpu):
    if "intel" in cpu.lower() or "amd" in cpu.lower():
        return "PC"
    
    if "arm" in cpu.lower():
        return "Rpi"
    
    return "Unknown"

def beautify_os_name(os):
    if "linux" in os.lower():
        return "Linux"
    
    if "win" in os.lower():
        return "Windows"
    
    return "unknown"

with tag("head"):
    doc.stag("link", rel="icon", href="static/img/logo.ico")
    doc.stag("meta", charset="UTF-8")
    with tag("style"):
        text("table, th, td{ \
                border:1px solid gray; \
                border-collapse: collapse;\
                } \
                .chapter { \
                  font-size: 180%; \
                  text-align: center; \
                  font-weight: bold; \
                } \
                \
                .description {\
                  padding: 1%; \
                  margin:auto; \
                  width: 70%; \
                  font-size:120%;\
                }\
                .tooltip {\
                  position: relative;\
                  display: block; \
                  font-size: 180%; \
                  text-align: center; \
                }\
                .tooltip .tooltiptext {\
                  visibility: hidden;\
                  background-color: rgba(255, 255, 255, 0.9);\
                  color: black;\
                  font-weight: normal;\
                  font-size: 70%;\
                  text-align: left;\
                  white-space: pre;\
                  border-radius: 6px;\
                  padding: 3px;\
                  border: 2px solid black;\
                  \
                  /* Position the tooltip */\
                  position: absolute;\
                  z-index: 1;\
                  top: 102%;\
                  left: 0%;\
                  margin-top: -1px;\
                }\
                .tooltip:hover .tooltiptext {\
                  visibility: visible; \
                }")

    with tag("title"):
        text("Byte Transpose Performance Tests")

with tag("body", style="background-image: url(\"static/img/prism.png\"); margin:0; padding:0; "):
    
    headers = ("Device", "OS", "Execution time [s]")
    functions = ReportReader(RESULTS_DIRECTORY, FUNCTION_DEFS_FILE).get_functions()

    with tag("header", style="/*background-color: rgba(0, 0, 0, 0.5);*/background: linear-gradient(180deg, rgba(2,0,36,0.5) 0%, rgba(168,168,168,0.5) 0%, rgba(255,255,255,0.5) 100%); color: black"):
        doc.stag("br")
        with tag("p", style="text-align: center; font-size: 250%; font-weight: bold;"):
            text("Performance tests of C functions")
        
        with tag("p", style="text-align: center; font-size: 120%;"):
            text("Project implemented in cooperation with Mirosław Żołądź phD at the AGH University of Science and Technology")

        with tag("div", style="margin: auto;"):
            with tag("table", style="margin: auto; border: 0px; font-size: 100%; font-weight: normal"): 
                doc.stag("col", width="250")
                doc.stag("col", width="250")
                with tag("tr", style="border: 0px"):
                    with tag("th", style="border: 0px"):
                        text("Sources: ")
                        with tag("a", href="https://github.com/FilipZajdel/ByteTranspose", style="text-decoration:none"):
                            text("Github")
                    with tag("th", style="border: 0px"):
                        text("Author: Filip Zajdel")
                    with tag("th", style="border: 0px"):
                        text("Contact: filipzajdel@student.agh.edu.pl")
        doc.stag("br")

    with tag("div", style="background: url(\"static/img/prism.png\") fixed; margin: auto; width: 70%; color: rgb(25, 20, 20); padding-left: 2%; padding-right: 2%; padding-top: 2%;"):

        doc.stag("br")
        doc.stag("br")
        with tag("div", klass="chapter"):
            text("-- About Tests --")
        with tag("div", klass="description"):
            text("The goal was to measure execution time of some pieces of C code across different devices,\
                    operating systems and compilers.")
        doc.stag("br")  

        with tag("div", klass="chapter"):
            text("-- Device Configuration --")
        with tag("div", klass="description"):
            text("Tests were executed on Raspberry Pi 4 (RPi) with Linux installed and one PC with both\
                Linux and Windows installed.")

        doc.stag("br")

        with tag("div", klass="chapter"):
            text("-- Results --")
        doc.stag("br"); doc.stag("br")

        for function in functions:

            function_details = function.get("details", "")
            function_body = "\n".join(function.get("body", ""))
            function_name = function["name"]
            vector_sizes = function["vector_sizes"]

            with tag("div", style="margin: auto; clear: both; font-size:100%; margin: left; width: 70%; border-top: solid 1px gray; /*border-left: solid 1px gray*/"):
                with tag("span", klass="tooltip"):
                    text(f"{function_name}()")

                    with tag("span", klass="tooltiptext"):
                        text(function_body)
                
                with tag("p", style="font-size: 120%; text-align: justify"):
                    text(function_details)

            with tag("div", style=f"margin: auto; text-align: center; width: 70%; font-size: 150%; border-radius: 10px"): 
                with tag("table", style="width: 100%; margin: auto; text-align: center"):
                    # Headers
                    with tag("tr"):
                        with tag("td", rowspan="2"):
                            text("Device")
                        with tag("td", rowspan="2"):
                            text("OS")
                        with tag("td", colspan=f"{len(vector_sizes)}"):
                            text("Execution time (MB/ms)")
                    # Vector sizes
                    with tag("tr"):
                        for size in vector_sizes:
                            with tag("td"):
                                text(size)
                    
                    for timing_info in function["timings"]:
                        with tag("tr"):
                            with tag("td"):
                                text(cpu_to_device(timing_info["device"]))
                            with tag("td"):
                                text(beautify_os_name(timing_info["platform"]))   
                            for size in vector_sizes:        
                                # print(timing_info["times"].get(size, 0))    
                                if size in timing_info["times"]:                   
                                    with tag("td"):
                                        text(round(timing_info["times"].get(size,0), 1))                        

                    # execution_times = []
                    # for func_info in func_info_list:
                    #     for func_data in func_info.get("data"):
                    #         pass
                            # with tag("tr"):
                            #     with tag("td", style="text-align:center"):
                            #         text(cpu_to_device(func_data.get("cpu")))
                            #     with tag("td", style="text-align:center"):
                            #         text(beautify_os_name(func_data.get("os")))
                            #     with tag("td", style="text-align:center; background-color: lightgrey; font-weight: bold"):
                            #         text(func_data.get("avg_time"))                


            # for idx, func_info in enumerate(func_info_list): 

            #     column_number = idx%2
            #     div_float = ""
            #     div_margin = ""
            #     if has_multiple_columns:
            #         div_float = "float: left;"
                
            #     if column_number == 1:
            #         div_margin = "margin-left: 2%;" 

            #     with tag("div", style=f"text-align: center; width: 49%; font-size: 150%; {div_float} {div_margin} border-radius: 10px"): #background-color: rgba(220, 220, 220, 0.3);
            #         vector_size = func_info.get("buffer_size")
            #         text(f"Test vector size: {vector_size}")

            #         with tag("table", style="width: 100%; margin: auto;"):
            #             with tag("tr", style="font-size: 120%"):
            #                 for header in headers[:len(headers)-1]:
            #                     with tag("th"):
            #                         text(header)
            #                 with tag("th", style="background-color: lightgrey"):
            #                     text(headers[-1])

            #             for func_data in func_info.get("data"):
            #                 with tag("tr"):
            #                     with tag("td", style="text-align:center"):
            #                         text(cpu_to_device(func_data.get("cpu")))
            #                     with tag("td", style="text-align:center"):
            #                         text(beautify_os_name(func_data.get("os")))
            #                     with tag("td", style="text-align:center; background-color: lightgrey; font-weight: bold"):
            #                         text(func_data.get("avg_time"))                

#             with tag("div", style="clear:both"): #Separator
#                 doc.stag("br")
#                 doc.stag("br")
#                 doc.stag("br")

with open("docs/index.html", "w") as html_file:
    html_file.write(doc.getvalue())
