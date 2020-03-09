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
        functions = {}

        for report in self.reports.values():
            for func_name, data in report.get("functions").items():

                function_body = function_defs.get(func_name, {}).get("body", "")
                function_details = function_defs.get(func_name, {}).get("details", "")
                buffer_size = data.get("buffer_size")
                function_data = self.__get_function_data(func_name, buffer_size, group_sort_by="cpu")
                function_entry = {"body"        : function_body, \
                                  "buffer_size" : buffer_size,   \
                                  "data"        : function_data, \
                                  "details"     : function_details}

                func_info_exists = False
                for func_data in functions.get(func_name, []):
                    if func_data.get("buffer_size") == buffer_size:
                        func_info_exists = True

                if not func_info_exists:
                    try:
                        functions[func_name].append(function_entry)
                    except KeyError:
                        functions[func_name] = []
                        functions[func_name].append(function_entry)

        return functions  

    def __get_function_data(self, function, buffer_size, group_sort_by=None):
        """ Returns list of tuples in format: [(CPU, OS, Num of repeats, Buffer size, Executed Time)] """
        data = []
        group_keys = ["cpu", "os", "compiler", "repeats", "buffer_size", "avg_time"]

        for report in self.reports.values():
            if function in report.get("functions", ""):
                if report["functions"].get(function).get("buffer_size", -1) == buffer_size:
                    time_elapsed = report["functions"].get(function).get("avg_time")
                    time_elapsed = round(time_elapsed, 1) if time_elapsed > 0.1 else round(time_elapsed, 2)
                    data.append({
                        "cpu" : report.get("cpu", ""), 
                        "os" : report.get("platform", ""), 
                        "compiler" : report.get("compiler", ""), 
                        "repeats" : report["functions"].get(function).get("repeats", ""),  
                        "avg_time" : time_elapsed
                    })
        
        if group_sort_by in group_keys:
            groups = []

            for d in data:
                value = d[group_sort_by]

                if value not in groups:
                    groups.append(value)
            
            groups=sorted(groups)
            new_data = []

            for group in groups:
                for d in data:
                    if d[group_sort_by] == group:
                        new_data.append(d)

            data = new_data

        return data

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

        for func_name, func_info_list in functions.items():

            function_details = func_info_list[0].get("details", "")
            function_body = "\n".join(func_info_list[0].get("body", ""))

            with tag("div", style="margin: auto; clear: both; font-size:100%; margin: left; width: 70%; border-top: solid 1px gray; /*border-left: solid 1px gray*/"):
                with tag("span", klass="tooltip"):
                    text(f"{func_name}()")

                    with tag("span", klass="tooltiptext"):
                        text(function_body)
                
                with tag("p", style="font-size: 120%; text-align: justify"):
                    text(function_details)
            
            has_multiple_columns = len(func_info_list) > 1

            for idx, func_info in enumerate(func_info_list): 

                column_number = idx%2
                div_float = ""
                div_margin = ""
                if has_multiple_columns:
                    div_float = "float: left;"
                
                if column_number == 1:
                    div_margin = "margin-left: 2%;" 

                with tag("div", style=f"text-align: center; width: 49%; font-size: 150%; {div_float} {div_margin} border-radius: 10px"): #background-color: rgba(220, 220, 220, 0.3);
                    vector_size = func_info.get("buffer_size")
                    text(f"Test vector size: {vector_size}")

                    with tag("table", style="width: 100%; margin: auto;"):
                        with tag("tr", style="font-size: 120%"):
                            for header in headers[:len(headers)-1]:
                                with tag("th"):
                                    text(header)
                            with tag("th", style="background-color: lightgrey"):
                                text(headers[-1])

                        for func_data in func_info.get("data"):
                            with tag("tr"):
                                with tag("td", style="text-align:center"):
                                    text(cpu_to_device(func_data.get("cpu")))
                                with tag("td", style="text-align:center"):
                                    text(beautify_os_name(func_data.get("os")))
                                with tag("td", style="text-align:center; background-color: lightgrey; font-weight: bold"):
                                    text(func_data.get("avg_time"))                

            with tag("div", style="clear:both"): #Separator
                doc.stag("br")
                doc.stag("br")
                doc.stag("br")

with open("docs/index.html", "w") as html_file:
    html_file.write(doc.getvalue())
