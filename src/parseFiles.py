# help
"""
    To run this tool independently...
    1. Type python to open python shell
    2. import parseFiles
    3. parseFiles.check_aliveness([path])

    for example, if you want a visual representation of the traceroute paths, you can pipe the output
    of your traceroutes in a file, this tool will parse them and create an intermediate representation
    and then use graphviz to generate a pdf file.
"""

#dependencies
"""
    To use install graphviz
        sudo pip install graphviz
"""

#imports
import os
import re
import socket
from graphviz import Digraph
import os


#globals
global_graph = {}

def my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def file_def_dict(path,file_name):
    file_data = {
        "filename":file_name,
        "path":os.path.join(path,file_name),
        "protocol": file_name.split("_")[2].split(".")[0],
        "port/type": file_name.split("_")[1],
        "domain": path.split("/")[len(path.split("/"))-2],
        "ip": file_name.split("_")[0]
    }
    return file_data

def parse_file(file_path):
    graph = []
    with open(file_path) as f:
        path_info = f.read().split("\n")
        for node in path_info:
            nodes = []
            for text in node.split(" "):
                if "(" in text or ")" in text:
                    text = text.strip("(")
                    text = text.strip(")")
                if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",text) and text not in nodes:
                    nodes.append(text)
                    if "*" in nodes:
                        nodes.remove("*")
                if text == "*" and "*" not in nodes and len(nodes) == 0:
                    nodes.append(text)
            graph.append(nodes)
    return graph


def add_to_global_graph(temp_representation):
    global global_graph
    temp_representation[0] = [my_ip()] 
    for i in range(len(temp_representation)-1):
        for node in temp_representation[i]:
            if node == "*":
                continue
            if node not in global_graph: 
                global_graph[node] = []
            for dest in temp_representation[i+1]:
                if dest in global_graph[node]:
                    continue
                global_graph[temp_representation[i][0]].append(dest)


def generate_graph(path):
    global global_graph
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    os.chdir("tmp")
    g = Digraph('path_graph', filename="{}_topology".format(path.split("/")[len(path.split("/"))-2]))
    
    for key in global_graph:
        #print key, global_graph[key]
        for dest in global_graph[key]:
            g.edge(key, dest)
    g.view()
"""
    @params
        string path (path to the directory that contains traceroute output files)
    @outputs
        none
    But this script generates two files in the temp folder, one is a graph representation that graphviz
    understand, and secondly it generates a pdf file that has the visual representation of the graph.
"""
def make_graph(path):
    print "parsing files..."
    # assuming that this directory contains valid and relevant files only.
    files_info = []
    for f in os.listdir(path):
        if f.endswith(".txt"):
            files_info.append(path + "/" + f)
    
    for file_dict in files_info:
        temp_representation = parse_file(file_dict)
        add_to_global_graph(temp_representation)
    print global_graph
    generate_graph(path)