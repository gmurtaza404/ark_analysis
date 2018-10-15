import os
from trace import Trace

dest_path_length = {}

def dict_add(key,value):
    if key not in dest_path_length:
        dest_path_length[key] = []
    dest_path_length[key] = dest_path_length[key] + [value]




def parse_data(file_name):
    with open(file_name, "rb") as f:
        data = f.read().split("\n")
        for line in data:
            if len(line) == 0:
                continue
            elif line[0] != "#":
                temp_trace = Trace()
                temp_trace.parse_sc_analysis_dump_line(line)
                dict_add(temp_trace.dest_addr,temp_trace.path_length)


def main():
    # crawl module directory
    root_directory = os.getcwd()
    
    os.chdir("module_anc") # TODO fix this hardcode

    for trace_file in os.listdir("."):
        print "Parsing {}".format(trace_file)
        if ".gz" in trace_file:
            os.system("gunzip {}".format(trace_file))
        
        os.system("sc_analysis_dump {} > decompressed.txt".format(trace_file ))
        parse_data("decompressed.txt")
    
    os.system("rm decompressed.txt")


    
    #print "Total Unique Addresses :" , len(dest_path_length.keys())
    for key in dest_path_length.keys():
        if len(dest_path_length[key]) > 1:
            print dest_path_length[key]
    
    os.chdir(root_directory)



main()




