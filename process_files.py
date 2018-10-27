"""
    Preprocessing the files, to convert it in a format thats easier to understand and play around with.
        This script set provides...
        1. load_file() function that loads the main file and returns a list of strings that contains the links to download the file.
        2. filter_file_by_team(), this function makes a folder for each team and divides the contents of main file into three different teams.
        3. filter_file_by_team_and_year() this function divides the data of a team into years.
        4. find_unique_modules() this function returns a list of modules that are unique in a given file.
        5. find_files_of_module() this function returns all files that belong to the given module name in the given file.
"""
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os,urllib,json
from multiprocessing import Pool
from trace import FileDescriptor,Trace
from sets import Set
from ark_analysis import ip_to_24subnet
# Globals
TEAMS = ["team-1","team-2","team-3"]
YEARS = ["2007", "2008", "2009", "2010", "2011","2012","2013","2014","2015","2016","2017"]

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
def apply_mask_on_ip_string(ip,mask_length):
    return ipbin_to_ipstring(apply_mask(ipstring_to_ipbin(ip),generate_subnet_mask(mask_length)))

def load_file(file_name):
    ret_list = []
    with open(file_name, "rb") as f:
        ret_list = f.read().split("\n")
    return ret_list


def filter_file_by_team(all_files, team_name):
    team_files = filter((lambda x: team_name in x), all_files)
    if not os.path.exists(team_name):
		os.makedirs(team_name)
    with open("./{}/{}.txt".format(team_name,team_name), "wb") as f:
        for team_file in team_files:
            f.write(team_file+ "\n")
    return team_files
    
def filter_file_by_team_and_years(all_files, team_name):
    all_year_files = []
    team_files = filter((lambda x: team_name in x), all_files)
    for year in YEARS:
        year_files = filter((lambda x: (year+"/") in x), team_files)
        all_files.append(year_files)
        with open("./{}/{}.txt".format(team_name,year), "wb") as f:
            for year_file in year_files:
                f.write(year_file+ "\n")
    return all_year_files


def find_unique_modules(path_to_file):
    modules = []
    with open(path_to_file, "rb") as f:
        data_files = f.read().split("\n")
        for data_file in data_files:
            file_name = data_file.split("/")[-1]
            if file_name != '':
                module_name = file_name.split(".")[5]
                if module_name not in modules:
                    modules.append(module_name)
    return modules
        
def find_files_of_module(path_to_file, name):
    files = []
    with open(path_to_file, "rb") as f:
        data_files = f.read().split("\n")
        for data_file in data_files:
            file_name = data_file.split("/")[-1]
            if file_name != '':
                module_name = file_name.split(".")[5]
                if module_name == name:
                    files.append(data_file)
    return files

def write_list_to_file(path_to_file, links_list):
    with open(path_to_file, "wb") as f:
        for link in links_list:
            f.write(link + "\n")

def get_file_name_from_link(link):
    return link.split("/")[-1]
def parse_file_name(file_name):
    name = file_name
    file_name = file_name.split(".")
    file_descriptor = FileDescriptor(file_name[1],file_name[2],file_name[3],file_name[4],file_name[5], name)
    return file_descriptor 

def get_unique_ips(path_to_file):
    unique_ips = Set([])
    with open(path_to_file, "rb") as f:
        data = f.read().split("\n")
        for line in data:
            if len(line) == 0:
                continue
            elif line[0] != "#":
                temp_trace = Trace()
                temp_trace.parse_sc_analysis_dump_line(line)
                if temp_trace.dest_replied == "R":
                    unique_ips.add(temp_trace)
    return unique_ips


def process_warts_file_for_unique_ips(path_to_file):
    directory_path = path_to_file.split("/")
    file_name = directory_path.pop()
    directory_path = "/".join(directory_path)
    root_directory = os.getcwd()
    if directory_path !=  '':
        os.chdir(directory_path)
    
    os.system("sc_analysis_dump {} > decompressed.txt".format(file_name))
    unique_ips = get_unique_ips("decompressed.txt")
    os.system("rm decompressed.txt")    
    os.chdir(root_directory)
    return unique_ips

def decompress_warts_gz_file(path_to_file):
    os.system("gunzip {}".format(path_to_file))

def process_files_in_folder_for_unique_ips(path_to_folder):
    # decompress files
    return_set = Set([])
    root_directory = os.getcwd()
    os.chdir(path_to_folder)
    all_files = os.listdir(".")
    print all_files
    for file_name in all_files:
        if ".gz" in file_name:
            print "Decompressing {}".format(file_name)
            decompress_warts_gz_file(file_name)
    all_files = os.listdir(".")
    for file_name in all_files:
        print "Processing {}".format(file_name)
        return_set = return_set.union(process_warts_file_for_unique_ips(file_name))
    os.chdir(root_directory)
    return return_set



def pool_function(cycle_name):
    print cycle_name
    cycle_unique_traces = process_files_in_folder_for_unique_ips(cycle_name)
    cycle_unique_traces = list(cycle_unique_traces)
    if len(cycle_unique_traces) == 0:
        return False
    with open("../cycle_ip_lists/{}.txt".format(cycle_name), "wb") as f:
        for trace in cycle_unique_traces:
            f.write(trace.dest_addr+ "," + str(trace.path_length) + "\n")
    return True





def main():
    print "processing files"
    # all_files = load_file("all_files.txt")
    # team1_files = filter_file_by_team(all_files,"team-1")
    # team2_files = filter_file_by_team(all_files,"team-2")
    # team3_files = filter_file_by_team(all_files,"team-3")
    # print len(team1_files), len(team2_files), len(team3_files)
    # team1_year_files = filter_file_by_team_and_years(all_files,"team-1")
    # team2_year_files = filter_file_by_team_and_years(all_files,"team-2")
    # team3_year_files = filter_file_by_team_and_years(all_files,"team-3")
    # all_modules = find_unique_modules("all_files.txt")
    # all_modules.sort()
    # print all_modules
    # team_1_anc_us_files = find_files_of_module("./team-1/2017.txt", "anc-us")
    # print len(team_1_anc_us_files)
    # #write_list_to_file("./team-1/team1-anc-us-files.txt",team_1_anc_us_files)
    # root = os.getcwd()
    # os.chdir("team-1")
    # if not os.path.exists("analysis"):
	#     os.makedirs("analysis")
    # os.chdir("analysis")

    # for link in team_1_anc_us_files:
    #     file_name = get_file_name_from_link(link)
    #     f_d = parse_file_name(file_name)
    #     #print f_d.cycle_id
    #     if not os.path.exists(f_d.cycle_id):
	# 	    os.makedirs(f_d.cycle_id)
    #     os.chdir(f_d.cycle_id)
        
    #     file_name_without_gz = f_d.name.split(".")
    #     file_name_without_gz.pop()
    #     file_name_without_gz = ".".join(file_name_without_gz)
            
    #     if f_d.name in os.listdir(".") or file_name_without_gz in os.listdir("."):
    #         print "Already downloaded {}".format(f_d.name)
    #     else:
    #         print "Downloading {}".format(f_d.name)
    #         os.system("axel -q {}".format(link))
    #     os.chdir("..")
        
    # os.chdir(root)
    # s1 = process_warts_file_for_unique_ips("./team-1/analysis/c005344/daily.l7.t1.c005344.20170101.anc-us.warts")
    # s2 = process_warts_file_for_unique_ips("./team-1/analysis/c005344/daily.l7.t1.c005344.20170102.anc-us.warts")
    
    # print len(s1) , len(s2), len(s1.union(s2)) , len(s1) + len(s2)
    os.chdir("./team-1/cycle_ip_lists")
    # cycle_unique_ips = list(process_files_in_folder_for_unique_ips("c005344"))
    # count = 0
    # for path in cycle_unique_ips:
    #     print path.path_length, path.request_ttl, (64 -int(path.reply_ttl))
    # print count, len(cycle_unique_ips)

    # for x in range(2000):
    #     if cycle_unique_ips[x].path_complete == "C":
    #         print cycle_unique_ips[x].dest_addr,cycle_unique_ips[x].dest_replied, cycle_unique_ips[x].path_complete
    #         cycle_unique_ips[x].p_print()
    #print count, len(cycle_unique_ips)
    # all_cycles = os.listdir(".")
    # p = Pool(4)
    # print (p.map(pool_function, all_cycles))
    # print "done"
    # union_of_all = Set([])
    
    # intersection_of_all = Set([])
    # total = 0
    # total_2 = 0
    # total_3 = 0
    # total_4 = 0
    # total_5 = 0
    # all_count = []
    dict_count = {}

    for cycle_list in os.listdir("."):
        with open(cycle_list, "rb") as f:
            print cycle_list
            temp_set = f.read().split("\n")
            temp_set.pop()
            for item in temp_set:
                ip, path_length = item.split(",")
                ip = apply_mask_on_ip_string(ip,25)
                try:
                    dict_count[ip].append(path_length)
                except KeyError:
                    dict_count[ip] = [path_length]
    
    # with open("../dict_count_path_len.json", "rb") as f:
    #     dict_count = json.loads(f.read())
    #count = 0
    # for key in dict_count.keys():
    #     if len(dict_count[key]) == 1:
    #         count += 1
    #         #print key, dict_count[key]
    # print len(dict_count.keys()), count
    # all_count = np.array(all_count)
    # print len(all_count)
    count_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for key in dict_count:
         count_array[len(dict_count[key])-1] += 1
    print sum(count_array) ,count_array
"""
    Analysis:
        Data from 1st January 2017 - 28th April 2017
        containing files of 106 cycles
        Total unique IPs 26,847,102
        Total Repeated IPs 127,666
              Repeated 2 Times -> 127273
              Repeated 3 Times -> 392
              Repeated 4 Times -> 1
              Repeated 5 Times -> 0
        No apparent repetitions in 4 months worth of data.
        
    Analysis on /24 subnets.
        Data from 1st January 2017 - 28th April 2017
        containing files of 106 cycles
        Total Unique /24 Subnets 10,019,550
        No repetitions -> 2,286,996
        Repeated 2 Times -> 2,848,270
        Repeated 3 Times -> 2,360,916
        Repeated 4 Times -> 1,420,166
        Repeated 5 Times -> 701,252
        Repeated 6 Times -> 271,581
        Repeated 7 Times -> 92,476
        Repeated 8 Times -> 27,863
        Repeated 10 Times -> 7,280
        Repeated 11 Times -> 1,716
        Repeated 12 Times -> 1,022
        Repeated 13 Times -> 12
"""
"""
    Analysis:
        Data from 1st January 2017 to 3rd October 2017 for probe anc-us
        This data contained 232 cycles
        Additional filters:
            1. Traces with non responsive destinations were filtered
        Total Unique IPs: 7900962
        Total IPs with at least 2 repetitions: 67961
        No repetitions -> 7833001
        Repeated 2 Times -> 67529
        Repeated 3 Times -> 429
        Repeated 4 Times -> 3
        Repeated 5 Times -> 0
        Repeated 6 Times -> 0
        

        With /31 Subnet
        Total Unique Subnets: 7847204
        No repetitions -> 7726471 
        Repeated 2 Times -> 119330
        Repeated 3 Times -> 1385
        Repeated 4 Times -> 18
        Repeated 5 Times -> 0
        Repeated 6 Times -> 0
        
        With /30 Subnet
        Total Unique Subnets: 7738706
        No repetitions -> 7513290 
        Repeated 2 Times -> 220281
        Repeated 3 Times -> 5036
        Repeated 4 Times -> 97
        Repeated 5 Times -> 2
        Repeated 6 Times -> 0
        
        With /29 Subnet
        Total Unique Subnets: 7532152
        No repetitions -> 7114189 
        Repeated 2 Times -> 399404
        Repeated 3 Times -> 17897
        Repeated 4 Times -> 640
        Repeated 5 Times -> 22
        Repeated 6 Times -> 0

        With /28 Subnet
        Total Unique Subnets: 7148202
        No repetitions -> 6396214 
        Repeated 2 Times -> 687650
        Repeated 3 Times -> 59820
        Repeated 4 Times -> 4223
        Repeated 5 Times -> 278
        Repeated 6 Times -> 17
        
        With /27 Subnet
        Total Unique Subnets: 6477526
        No repetitions -> 5223119 
        Repeated 2 Times -> 1048714
        Repeated 3 Times -> 177602
        Repeated 4 Times -> 24851
        Repeated 5 Times -> 2874
        Repeated 6 Times -> 332
        Repeated 7 Times -> 33
        Repeated 8 Times -> 1
        
        With /26 Subnet
        Total Unique Subnets: 5429332
        No repetitions -> 3612490 
        Repeated 2 Times -> 1272985
        Repeated 3 Times -> 403687
        Repeated 4 Times -> 108568
        Repeated 5 Times -> 25366
        Repeated 6 Times -> 5123
        Repeated 7 Times -> 930
        Repeated 8 Times -> 161
        Repeated 9 Times -> 21
        Repeated 10 Times -> 1

        With /25 Subnet
        Total Unique Subnets: 4078270
        No repetitions -> 1986363 
        Repeated 2 Times -> 1272985
        Repeated 3 Times -> 1055572
        Repeated 4 Times -> 566976
        Repeated 5 Times -> 278551
        Repeated 6 Times -> 120984
        Repeated 7 Times -> 46734
        Repeated 8 Times -> 16018
        Repeated 9 Times -> 5080
        Repeated 10 Times -> 1455
        Repeated 11 Times -> 407
        Repeated 12 Times -> 101
        Repeated 13 Times -> 26
        Repeated 14 Times -> 1
        Repeated 15 Times -> 2
        
        With /24 Subnet
        Total Unique Subnets: 2737134
        No repetitions -> 913132 
        Repeated 2 Times -> 564942
        Repeated 3 Times -> 403465
        Repeated 4 Times -> 298537
        Repeated 5 Times -> 215601
        Repeated 6 Times -> 146157
        Repeated 7 Times -> 90911
        Repeated 8 Times -> 52215
        Repeated 9 Times -> 27566
        Repeated 10 Times -> 13719
        Repeated 11 Times -> 6242
        Repeated 12 Times -> 2767
        Repeated 13 Times -> 1134
        Repeated 14 Times -> 451
        Repeated 15 Times -> 61
        Repeated 16 Times -> 19
        Repeated 17 Times -> 1
        
"""


main()
#print 

























