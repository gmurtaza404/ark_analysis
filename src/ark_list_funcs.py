"""
    fluctuation(list), returns fluctuation of data points in that list.

"""
import os, map_reduce, multiprocessing
import numpy as np
import pandas as pd
from trace import Trace,FileDescriptor
from utilities import *
from multiprocessing.pool import ThreadPool
from random import *
import collections
from ast import literal_eval as make_tuple
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
from list_manip import *
import socket
import parseFiles

def filter_by_team_name(all_files, team_name):
    return filter((lambda x: team_name in x), all_files)
    
def filter_files_by_year(all_files, year):
    return filter((lambda x: year in x), all_files)

def find_files_of_module(all_files, name):
    return filter((lambda x: name == parse_file_name(get_file_name_from_link(x)).module_name), all_files)


def parse_file_name(file_name):
    name = file_name
    file_name = file_name.split(".")
    file_descriptor = FileDescriptor(file_name[1],file_name[2],file_name[3],file_name[4],file_name[5], name)
    return file_descriptor 

def parse_sc_analysis_dump_file(path_to_file):
    parsed_list = []
    file_data = load_file(path_to_file)
    if not len(file_data):
        return file_data
    # filter header data
    file_data = filter(lambda x: len(x) > 0 and x[0] != '#', file_data)
    for data in file_data:
        temp_trace = Trace()
        temp_trace.parse_sc_analysis_dump_line(data)
        if temp_trace.dest_replied == "R":
            parsed_list.append((temp_trace.dest_addr, (temp_trace.timestamp, temp_trace.path_length, temp_trace.path_complete)))
    return parsed_list

def process_warts_file(path_to_file):
    directory_path = get_directory(path_to_file)
    if ".gz" in path_to_file:
        path_to_file = decompress_warts_gz_file(path_to_file)
    parsed_file_name = directory_path + str(randint(0,10000000))+".txt"
    os.system("sc_analysis_dump {} > {}".format(path_to_file,parsed_file_name))
    parsed_data = parse_sc_analysis_dump_file(parsed_file_name)
    os.system("rm {}".format(parsed_file_name))
    return parsed_data

def stub_reduce(x):
    return x

def fluctutaion(temp_list):
    return np.mean(map(lambda x: abs(x - temp_list[0]),temp_list)[1:])


def process_cycle_folder(path_to_folder, results_folder = "/home/fatima/Documents/internet_measurements/ark_analysis/team-1/results"):
    cycle_id = get_file_name_from_link(path_to_folder)
    print "Processing : {}...".format(cycle_id)
    
    file_paths = map(lambda x: path_to_folder +"/" + x, os.listdir(path_to_folder))
    cycle_data = collections.defaultdict(list)

    for file_path in file_paths:
        filedata = process_warts_file(file_path)
        for data in filedata:
            key, value = data
            cycle_data[key].append(value)
                    
    print "Writing : {}...".format(cycle_id)
    write_tuple_to_file( (cycle_id,cycle_data.items()), results_folder)
    del cycle_data
    return True

def write_tuple_to_file(data_tuple, directory_path):
    file_name, data = data_tuple
    write_tuple_on_file(directory_path+"/"+file_name + ".csv", data)


def process_all_cycle_folders(path_to_folder,results_folder,chunksize = 1):
    pool = multiprocessing.Pool(None)
    folder_paths = map(lambda x: path_to_folder +"/" + x, os.listdir(path_to_folder))
    map_responses = pool.map(process_cycle_folder, folder_paths, chunksize=chunksize)
    print map_responses

def aggregate_all_cycle_files(path_to_folder, result_folder, chunksize = 1):
    file_paths = map(lambda x: path_to_folder +"/" + x, os.listdir(path_to_folder))
    agg_data = collections.defaultdict(list)
    for file_path in file_paths:
        data = read_tuple_file(file_path)
        for key, value in data:
            agg_data[key].append(value)
    write_tuple_to_file(("agg_data",agg_data.items()), result_folder)


def process_aggregated_list(path_to_file, result_folder):
    temp_list = []
    with open(path_to_file, "rb") as f:
        rows = f.read().split("\n")
        for row in rows:
            if len(row.split("\t")) > 3:
                data = row.split("\t")
                data.pop()
                key = data[0]
                values = sorted(data[1:], key=lambda x: make_tuple(x)[0] )
                time_fluc = fluctutaion(map((lambda x: int(make_tuple(x)[0]) ), values))/(60.0*60*24)
                path_fluc = fluctutaion(map((lambda x: int(make_tuple(x)[1]) ), values))            
                temp_list.append([key, path_fluc, time_fluc, values])
    
    ##print map((lambda x: x[0]), temp_list)
    df = pd.DataFrame({"ip": map((lambda x: x[0]), temp_list), "path_fluc": map((lambda x: x[1]), temp_list), "time_fluc": map((lambda x: x[2]), temp_list), "data": map((lambda x: x[3]), temp_list)})
    df.to_csv("{}/procesed_agg_result.csv".format(result_folder), sep='\t', encoding='utf-8')


def analysis_aggregated_list(path_to_file, results_folder):
    df = pd.read_csv(path_to_file, sep="\t")
    asns = []
    for index, row in df.iterrows():
        if row['path_fluc'] > 13:
            print row["ip"]

def run_traceroutes_on_anomalous_ips(path_to_file):
    ips = load_file(path_to_file)
    for ip in ips:
        print ip
        os.system("traceroute {}  -m 100 > ./traceroute_data/{}.txt".format(ip, ip))
    
    
def make_graph(path_to_traceroute_files):
    parseFiles.make_graph(path_to_traceroute_files)