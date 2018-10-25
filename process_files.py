"""
    Preprocessing the files, to convert it in a format thats easier to understand and play around with.
        This script set provides...
        1. load_file() function that loads the main file and returns a list of strings that contains the links to download the file.
        2. filter_file_by_team(), this function makes a folder for each team and divides the contents of main file into three different teams.
        3. filter_file_by_team_and_year() this function divides the data of a team into years.
        4. find_unique_modules() this function returns a list of modules that are unique in a given file.
        5. find_files_of_module() this function returns all files that belong to the given module name in the given file.
26718937
26847102
"""

import os,urllib
from trace import FileDescriptor,Trace
from sets import Set

# Globals
TEAMS = ["team-1","team-2","team-3"]
YEARS = ["2007", "2008", "2009", "2010", "2011","2012","2013","2014","2015","2016","2017"]


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
                unique_ips.add(temp_trace.dest_addr)
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
    # write_list_to_file("./team-1/team1-anc-us-files.txt",team_1_anc_us_files)
    # root = os.getcwd()
    # os.chdir("team-1")
    # if not os.path.exists("analysis"):
	# 	os.makedirs("analysis")
    # os.chdir("analysis")

    # for link in team_1_anc_us_files:
    #     file_name = get_file_name_from_link(link)
    #     f_d = parse_file_name(file_name)
    #     #print f_d.cycle_id
    #     if not os.path.exists(f_d.cycle_id):
	# 	    os.makedirs(f_d.cycle_id)
        
    #     print "Downloading to ... -> ./{}/{}".format(f_d.cycle_id,f_d.name)
    #     urllib.urlretrieve(link, "./{}/{}".format(f_d.cycle_id,f_d.name))

    # os.chdir(root)
    # s1 = process_warts_file_for_unique_ips("./team-1/analysis/c005344/daily.l7.t1.c005344.20170101.anc-us.warts")
    # s2 = process_warts_file_for_unique_ips("./team-1/analysis/c005344/daily.l7.t1.c005344.20170102.anc-us.warts")
    
    # print len(s1) , len(s2), len(s1.union(s2)) , len(s1) + len(s2)
    os.chdir("./team-1/cycle_ip_lists")
    # print os.listdir(".")
    # for cycle_name in os.listdir("."):
    #     print cycle_name
    #     cycle_unique_ips = process_files_in_folder_for_unique_ips(cycle_name)
    #     cycle_unique_ips = list(cycle_unique_ips)
    #     if len(cycle_unique_ips) == 0:
    #         continue
    #     with open("../cycle_ip_lists/{}.txt".format(cycle_name), "wb") as f:
    #         for ip in cycle_unique_ips:
    #             f.write(ip + "\n")
    union_of_all = Set([])
    intersection_of_all = Set([])
    total = 0
    for cycle_list in os.listdir("."):
        with open(cycle_list, "rb") as f:
            print cycle_list
            temp_set = Set(f.read().split("\n"))
            total = total + len(temp_set)
            #union_of_all = union_of_all.union(temp_set)
            #intersection_of_all = intersection_of_all.intersection(temp_set)
    print total

    


main()




























