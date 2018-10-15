from trace import Trace


def main():
    with open("decoded_data_1.txt", "rb") as f:
        data = f.read().split("\n")
        for line in data:
            if len(line) == 0:
                continue
            if line[0] != "#":
                temp_trace = Trace()
                temp_trace.parse_sc_analysis_dump_line(line)
                print temp_trace.src_addr, temp_trace.dest_addr, temp_trace.path_length

main()




