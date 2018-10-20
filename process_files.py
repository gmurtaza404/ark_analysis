"""
    Preprocessing the files, to convert it in a format thats easier to understand and play around with.
        This script set provides...
        1. load_file() function that loads the main file and returns a list of strings that contains the links to download the file.
        2. filter_file_by_team(), this function makes a folder for each team and divides the contents of main file into three different teams.
        3. filter_file_by_team_and_year() this function divides the data of a team into years.
        4. find_unique_modules() this function returns a list of modules that are unique in a given file.
        5. find_files_of_module() this function returns all files that belong to the given module name in the given file.
"""

import os
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
    print len(find_files_of_module("all_files.txt", "anc-us"))

main()




























