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
from src import map_reduce, utilities, ark_list_funcs
# Globals
TEAMS = ["team-1","team-2","team-3"]    
YEARS = ["2007", "2008", "2009", "2010", "2011","2012","2013","2014","2015","2016","2017"]
path = "/home/fatima/Documents/internet_measurements/ark_analysis/team-1/analysis"
results = "/home/fatima/Documents/internet_measurements/ark_analysis/team-1/results"

ark_list_funcs.make_graph("./traceroute_data")