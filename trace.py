from datetime import datetime

class FileDescriptor(object):
    """
        1. List ID      (uint)
        2. Team ID      (uint)
        3. Cycle ID     (unit)
        4. Date         (string)
        5. Module Name  (string)
        6. Name         (string)
    """
    def __init__(self,l_id,t_id,c_id,date,m_name, name):
        self.list_id = l_id
        self.team_id = t_id
        self.cycle_id = c_id
        self.date_string = date
        self.module_name = m_name
        self.name = name
    def p_print(self):
        print "List ID: {}\nTeam ID: {}\nCycle ID: {}\nDate: {}\nModule Name: {}".format(self.list_id,self.team_id,self.cycle_id,self.date_string,self.module_name)
        print "File Name: {}".format(self.name)
        

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



# =======================================================================
# This file contains an ASCII representation of the IP paths stored in
# the binary skitter arts++ and scamper warts file formats.
#
# This ASCII file format is in the sk_analysis_dump text output
# format: imdc.datcat.org/format/1-003W-7
#
# =======================================================================
# There is one trace per line, with the following tab-separated fields:
#
#
#  1. Key -- Indicates the type of line and determines the meaning of the
#            remaining fields.  This will always be 'T' for an IP trace.
#
# -------------------- Header Fields ------------------
#
#  2. Source -- Source IP of skitter/scamper monitor performing the trace.
#
#  3. Destination -- Destination IP being traced.
#
#  4. ListId -- ID of the list containing this destination address.
#
#        This value will be zero if no list ID was provided.  (uint32_t)
#
#  5. CycleId -- ID of current probing cycle (a cycle is a single run
#                through a given list).  For skitter traces, cycle IDs
#                will be equal to or slightly earlier than the timestamp
#                of the first trace in each cycle. There is no standard
#                interpretation for scamper cycle IDs.
#
#        This value will be zero if no cycle ID was provided.  (uint32_t)
#
#  6. Timestamp -- Timestamp when trace began to this destination.
#
# -------------------- Reply Fields ------------------
#
#  7. DestReplied -- Whether a response from the destination was received.
#
#        R - Replied, reply was received
#        N - Not-replied, no reply was received;
#            Since skitter sends a packet with a TTL of 255 when it halts
#            probing, it is still possible for the final destination to
#            send a reply and for the HaltReasonData (see below) to not
#            equal no_halt.  Note: scamper does not perform last-ditch
#            probing at TTL 255 by default.
#
#  8. DestRTT -- RTT (ms) of first response packet from destination.
#        0 if DestReplied is N.
#
#  9. RequestTTL -- TTL set in request packet which elicited a response
#      (echo reply) from the destination.
#        0 if DestReplied is N.
#
# 10. ReplyTTL -- TTL found in reply packet from destination;
#        0 if DestReplied is N.
#
# -------------------- Halt Fields ------------------
#
# 11. HaltReason -- The reason, if any, why incremental probing stopped.
#
# 12. HaltReasonData -- Extra data about why probing halted.
#
#        HaltReason            HaltReasonData
#        ------------------------------------
#        S (success/no_halt)    0
#        U (icmp_unreachable)   icmp_code
#        L (loop_detected)      loop_length
#        G (gap_detected)       gap_limit
#
# -------------------- Path Fields ------------------
#
# 13. PathComplete -- Whether all hops to destination were found.
#
#        C - Complete, all hops found
#        I - Incomplete, at least one hop is missing (i.e., did not
#            respond)
#
# 14. PerHopData -- Response data for the first hop.
#
#       If multiple IP addresses respond at the same hop, response data
#       for each IP address are separated by semicolons:
#
#       IP,RTT,nTries                   (for only one responding IP)
#       IP,RTT,nTries;IP,RTT,nTries;... (for multiple responding IPs)
#
#         where
#
#       IP -- IP address which sent a TTL expired packet
#       RTT -- RTT of the TTL expired packet
#       nTries -- number of tries before response received from hop
#
#       This field will have the value 'q' if there was no response at
#       this hop.
#
# 15. PerHopData -- Response data for the second hop in the same format
#       as field 14.
#
# ...
#
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
        self.timestamp = int(dump_line[5])
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
        if self.dest_replied == "R":
            dest_hop = Hop()
            dest_hop.parse_hop_string("{},{},{}".format(self.dest_addr,self.dest_rtt,1))
        
        self.path_length = len(self.path_hops)

    def p_print(self):
        print "*****************************************************************************"
        print "Source Addr      : ", self.src_addr
        print "Destination Addr : ", self.dest_addr
        print "Trace Date       : ", datetime.utcfromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print "Trace Length     : ", self.path_length
        print "Dest Replied     : ", self.dest_replied
        print "Path Complete    : ", self.path_complete
        
        
        print "Hops ..."
        hop_count = 1
        for hop in self.path_hops:
            print "{}.-------------------------".format(hop_count)
            hop.p_print()
            hop_count += 1
        print "*****************************************************************************"