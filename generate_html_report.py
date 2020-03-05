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

                function_body = function_defs.get(func_name, "")
                buffer_size = data.get("buffer_size")
                function_data = self.__get_function_data(func_name, buffer_size, group_by="cpu")
                function_entry = {"body"        : function_body, \
                                  "buffer_size" : buffer_size,   \
                                  "data"        : function_data}

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

    def __get_function_data(self, function, buffer_size, group_by=None):
        """ Returns list of tuples in format: [(CPU, OS, Num of repeats, Buffer size, Executed Time)] """
        data = []
        group_keys = ["cpu", "os", "compiler", "repeats", "buffer_size", "avg_time"]

        for report in self.reports.values():
            if function in report.get("functions", ""):
                if report["functions"].get(function).get("buffer_size", -1) == buffer_size:
                    time_elapsed = report["functions"].get(function).get("avg_time")
                    time_elapsed = expsec_to_sec_suffix(time_elapsed)
                    data.append({
                        "cpu" : report.get("cpu", ""), 
                        "os" : report.get("platform", ""), 
                        "compiler" : report.get("compiler", ""), 
                        "repeats" : report["functions"].get(function).get("repeats", ""),  
                        "avg_time" : time_elapsed
                    })
        
        if group_by in group_keys:
            groups = []

            for d in data:
                value = d[group_by]

                if value not in groups:
                    groups.append(value)
            new_data = []

            for group in groups:
                for d in data:
                    if d[group_by] == group:
                        new_data.append(d)

            data = new_data

        return data

    def get_functions(self):
        return self.__functions


def expsec_to_sec_suffix(val, precision=3):
    if val > 1:
        return f"{round(val, precision)}s"
    elif val > 10**(-3):
        return f"{round(val/(10**(-3)), precision)}ms"
    elif val > 10**(-6):
        return f"{round(val/(10**(-6)), precision)}µs"
    elif val > 10**(-9):
        return f"{round(val/(10**(-9)), precision)}ns"
    else:
        return f"{val}"

def cpu_to_device(cpu):
    if "intel" in cpu.lower() or "amd" in cpu.lower():
        return "PC"
    
    if "arm" in cpu.lower():
        return "Rpi"
    
    return "Unknown"



with tag("head"):
    doc.stag("link", rel="icon", href="static/img/logo.ico")
    doc.stag("meta", charset="UTF-8")
    doc.asis(
        "<style>table,th,td{border:2px solid gray; border-collapse: collapse}</style>")

    with tag("title"):
        text("Byte Transpose Performance Tests")

with tag("body", style="background: url(\"static/img/prism.png\") fixed; color: black"):
    
    headers = ("Device", "OS", "Execution time")
    functions = ReportReader(RESULTS_DIRECTORY, FUNCTION_DEFS_FILE).get_functions()

    with tag("div", style="margin: auto; width: 75%; color: rgb(25, 20, 20)"):
        with tag("div", style="font-size: 180%; text-align: center;"):
            text("-- About Tests --")
        with tag("div", style="font-size:120%; background-color: rgba(220, 220, 220, 0.3); border-radius: 10px"):
            text("The goal was to measure execution time of some pieces of C code across different devices,\
                    operating systems and compilers.")
        doc.stag("br")  

        with tag("div", style="font-size: 180%; text-align: center;"):
            text("-- Device Configuration --")
        with tag("div", style="font-size:120%; background-color: rgba(220, 220, 220, 0.3); border-radius: 10px"):
            text("Tests were executed on Raspberry Pi 4 (RPi) with Linux installed and one PC with both\
                Linux and Windows installed.")

        doc.stag("br")

        with tag("div", style="font-size: 180%; text-align: center;"):
            text("-- Results --")
        doc.stag("br"); doc.stag("br")

        for func_name, func_info_list in functions.items():
            with tag("div", style="font-size:180%; font-weight: bold; text-align: center"):
                text(f"{func_name}()")
            
            has_multiple_columns = len(func_info_list) > 1 

            for idx, func_info in enumerate(func_info_list):

                column_number = idx%2
                div_float = ""
                div_margin = ""
                if has_multiple_columns:
                    div_float = "float: left;"
                
                if column_number == 1:
                    div_margin = "margin-left: 2%;"

                with tag("div", style=f"text-align: center; width: 48%; font-size: 150%; {div_float} {div_margin} background-color: rgba(220, 220, 220, 0.3); border-radius: 10px"):
                    vector_size = func_info.get("buffer_size")
                    text(f"Test vector size: {vector_size}")

                    with tag("table", style="width: 100%; margin: auto"):
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
                                    text(func_data.get("os"))
                                with tag("td", style="text-align:center; background-color: lightgrey; font-weight: bold"):
                                    text(func_data.get("avg_time"))        

                    doc.stag("br")         

                if idx == 1:
                    with tag("div", style="clear:both"):
                        doc.stag("br")


            with tag("div", style="clear:both"):
                doc.stag("br")
                doc.stag("br")            


with open("docs/index.html", "w") as html_file:
    html_file.write(doc.getvalue())
