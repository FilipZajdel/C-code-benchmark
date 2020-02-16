from yattag import Doc
import os
import json

doc, tag, text = Doc().tagtext()

def load_json_reports(directory):
    files = [d for d in os.listdir(directory) if ".json" in d]
    merged_report = {}

    for report in files:
        with open(f"{directory}/{report}", "r") as fp:
            merged_report[report] = json.load(fp)

    return merged_report


def get_function_names(reports):
    names = []

    for report in reports.values():
        for func_name in report.get("functions"):
            if func_name not in names:
                names.append(func_name)

    return names

def get_data_of_function(reports, function, group = False, group_key=None):
    """ Returns list of tuples in format: [(CPU, OS, Num of repeats, Buffer size, Executed Time)] """
    data = []
    group_keys = ["cpu", "os", "repeats", "buffer_size", "avg_time"]

    for report in reports.values():
        if function in report.get("functions", ""):
            cpu = report.get("cpu", "")    
            os = report.get("platform", "")
            repeats = report["functions"].get(function).get("repeats", "")
            buffer_size = report["functions"].get(function).get("buffer_size", "-")
            time_elapsed = report["functions"].get(function).get("avg_time")
            time_elapsed = expsec_to_sec_postfix(time_elapsed)
            data.append((cpu, os, repeats, buffer_size, time_elapsed))
    
    if group and group_key in group_keys:
        groups = []
        idx_of_group = group_keys.index(group_key)

        for d in data:
            value = d[idx_of_group]

            if value not in groups:
                groups.append(value)
        new_data = []

        for gr in groups:
            for d in data:
                if d[idx_of_group] == gr:
                    new_data.append(d)

        data = new_data

    return data

def expsec_to_sec_postfix(val, precision=3):
    if val > 1:
        return f"{round(val, precision)}s"
    elif val > 10**(-3):
        return f"{round(val/(10**(-3)), precision)}ms"
    elif val > 10**(-6):
        return f"{round(val/(10**(-6)), precision)}µs"
    elif val >> 10**(-9):
        return f"{round(val/(10**(-9)), precision)}µs"

with tag("head"):
    doc.stag("link", rel="icon", href="static/img/logo.ico")
    doc.stag("meta", charset="UTF-8")
    doc.asis(
        "<style>table,th,td{border:2px solid gray; border-collapse: collapse}</style>")

with tag("body", style="background: url(\"static/img/prism.png\") fixed; color: black"):
    with tag("title"):
        text("Byte Transpose Performance Tests")
    
    headers = ("CPU", "OS", "Number of Repeats", "Buffer size", "Execution time")
    reports = load_json_reports("Results")
    functions = get_function_names(reports)

    with tag("div", style="margin: auto; width: 75%; text-align: center"):
        with tag("h", style="font-size: 150%; font-color: rgb(99,91,88)"):
            text("Summary of timing tests of C functions on different operating systems and CPUs")
        
        doc.stag("br")        
        doc.stag("hr")
        doc.stag("br")  

        for function in functions:
            with tag("h", style="font-size:200%; font-color: rgb(99,91,88)"):
                text(function)
            with tag("table", style="width: 100%"):
                with tag("tr", style="font-size: 120%"):
                    for header in headers:
                        with tag("th"):
                            text(header)

                for data_set in get_data_of_function(reports, function, group=True, group_key="buffer_size"):
                    with tag("tr"):
                        for column in data_set:
                            with tag("td", style="text-align:center"):
                                text(column)
                       
            doc.stag("br")
            doc.stag("br")

with open("docs/index.html", "w") as html_file:
    html_file.write(doc.getvalue())
