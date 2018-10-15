class Destination(object):
    """
        Destination object contains three fields
            1.IP Address
            2.RTT
            3.Number of tries
    """
    def __init__(self,_ip,_rtt,_ntries):
        self.addr = _ip
        self.rtt = _rtt
        self.ntries = _ntries
    
    # Pretty print destination
    def p_print(self):
        print "Address: {}\nRTT: {}\nNumber of Tries: {}".format(self.addr,self.rtt,self.ntries)



class Hop(object):
    """
        Hop object can contain multiple Destination objects
    """
    def __init__(self):
        self.destinations = []
    
    def add_destination(self,dest):
        self.destinations.append(dest)
    
    # Parse Hop data of sc_analysis_dump file
    def parse_hop_string(self,hop_line):
        hop_line = hop_line.split(";")
        for dst in hop_line:
            dst = dst.split(",")
            if len(dst) < 3:
                self.destinations.append(Destination("*", "-1", "-1"))
            else:
                self.destinations.append(Destination(dst[0],dst[1],dst[2]))

    # Pretty print for Hop class
    def p_print(self):
        for dest in self.destinations:
            dest.p_print()
    # Number of destinations at this hop
    def num_destinations(self):
        return len(self.destinations)




"""
    #TODO Write a description of Trace class
"""

class Trace(object):
    """
        Instantiates a stub trace object
    """
    def __init__(self):
        self.key = ""
        # Header Fields
        self.src_addr = ""              #str
        self.dest_addr = ""             #str
        self.list_id = -1               #uint_32
        self.cycle_id = -1              #uint_32
        self.timestamp = ""             #timestamp
        # Reply Fields
        self.dest_replied = ""          # R/N R-> Replied, N-> Not-replied, no reply was received
        self.dest_rtt = -1              # RTT on the return packet, this field is 0 if dest_replied = 'N'
        self.request_ttl = -1           # TTL on the request packet, this field is 0 if dest_replied = 'N'
        self.reply_ttl = -1             # TTL on the reply packet, this field is 0 if dest_replied = 'N'
        # Halt Fields
        self.halt_reason = ""           # Reason if any.
        self.halt_reason_data = ""      # Additional Data on why halt occured. S -> Sucess, U -> Unreachable, L-> Loop Detected, G-> Gap Detected
        # Path Fields
        self.path_complete = ""         # Whether all hops to the destinations were found. C-> Complete, I-> Incomplete
        self.path_hops = []             # List of hops in the trace.
        # Derived Fields
        self.path_length = -1
    """
        Parse a line of sc_analysis dump file
    """
    def parse_sc_analysis_dump_line(self,dump_line):
        dump_line = dump_line.split("\t")
        self.key = dump_line[0]
        self.src_addr = dump_line[1]
        self.dest_addr = dump_line[2]
        self.list_id = dump_line[3]
        self.cycle_id = dump_line[4]
        self.timestamp = dump_line[5]
        self.dest_replied = dump_line[6]
        self.dest_rtt = dump_line[7]
        self.request_ttl = dump_line[8]
        self.reply_ttl = dump_line[9]
        self.halt_reason = dump_line[10]
        self.halt_reason_data = dump_line[11]
        self.path_complete = dump_line[12]
        
        path_string = dump_line[13:]
        for hop_string in path_string:
            temp_hop = Hop()
            temp_hop.parse_hop_string(hop_string)
            self.path_hops.append(temp_hop)
        
        self.path_length = len(self.path_hops)