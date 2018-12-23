"""
    load_file(path_to_file), reads a file and parses a list and returns it.
    decompress_warts_gz_file(path_to_file), unzips a .gz file.
    make_cdf(data_list), returns a x and y coordinates of a cdf graph
    make_graph_file(x,y,output_file), writes the data points in a csv file.
"""

import os, json
import numpy as np
import pandas as pd
from ast import literal_eval as make_tuple
import matplotlib.pyplot as plt


def parse_values(values):
    ret_string = ""
    for value in values:
        ret_string = ret_string + str(value) + "\t"
    return ret_string



def update_last_file_in_path(path_to_file, new_name):
    path_to_file =path_to_file.split("/")
    path_to_file[-1] = new_name
    return "/".join(path_to_file)

def remove_file_extension(file_name):
    file_name = file_name.split(".")
    file_name.pop(-1)
    file_name = ".".join(file_name)
    return file_name

def make_graph_file(x,y, output_file_path):
    data_frame = {"x_axis": x, "y_axis": y}
    df = pd.DataFrame(data = data_frame)
    df.to_csv(output_file_path, sep='\t', encoding='utf-8')

def make_cdf(data_list):
    x = np.sort(data_list)
    y = np.arange(len(x))/float(len(x))
    return x,y

def load_file(file_name):
    ret_list = []
    with open(file_name, "rb") as f:
        ret_list = f.read().split("\n")
    return ret_list

def write_list_to_file(path_to_file, links_list):
    with open(path_to_file, "wb") as f:
        for link in links_list:
            f.write(str(link) + "\n")
def write_tuple_on_file(path_to_file, data_list):
    with open(path_to_file, "wb") as f:
        for data in data_list:
            key, values = data
            f.write(key + "\t"  + parse_values(values)+ "\n")

def read_tuple_file(path_to_file):
    return_list = []
    with open(path_to_file, "rb") as f:
        data_list = f.read().split("\n")
        data_list.pop()
        for data in data_list:
            key = data.split("\t")[0]
            value = make_tuple(data.split("\t")[1])
            return_list.append((key, value))
    return return_list


def decompress_warts_gz_file(path_to_file):
    os.system("gunzip {}".format(path_to_file))
    return update_last_file_in_path(path_to_file, remove_file_extension(get_file_name_from_link(path_to_file)))

def get_file_name_from_link(link):
    return link.split("/")[-1]

def apply_mask_on_ip_string(ip,mask_length):
    return ipbin_to_ipstring(apply_mask(ipstring_to_ipbin(ip),generate_subnet_mask(mask_length)))

def get_directory(path_to_file):
    path_list = path_to_file.split("/")
    path_list.pop()
    if len(path_list):
        path_list[len(path_list)-1] = path_list[len(path_list)-1] + "/"
    directory_to_write_in = "/".join((path_list))
    return directory_to_write_in


"""
    IP MANIPULATION FUNCTIONS
"""
def ipstring_to_ipbin(ip):
    ip = ip.split(".")
    ret_binary = ""
    for part in ip:
        part = int(part)
        bin_part =  '0'*(8-len(bin(part)[2:]))+bin(part)[2:]
        ret_binary = ret_binary + bin_part
    return ret_binary
def generate_subnet_mask(length):
    return '1'*(length)+'0'*(32-length)
def apply_mask(ip, subnet_mask):
    ip = int(ip,2)
    subnet_mask = int(subnet_mask,2)
    int_representation = ip&subnet_mask
    return '0'*(32-len(bin(int_representation)[2:]))+bin(int_representation)[2:]
def ipbin_to_ipstring(ip):
    ret_string = []
    for x in xrange(0,32,8):
        ret_string.append(str(int(ip[x:x+8],2)))
    return ".".join(ret_string)

"""
    Graphing Utilities
"""

def make_scatter_plot(x,y,x_label,y_label):
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.scatter(x, y)
    plt.show()

def plot_cdf(data, x_label, xlims, xlime):
    x, y = make_cdf(data)
    plt.xlabel(x_label)
    plt.xlim((xlims,xlime))
    plt.ylabel("CDF")
    plt.plot(x, y)
    plt.show()
