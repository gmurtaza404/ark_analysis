"""
    This script provides two main functions.
        1. find_geo_diversity(path_to_file), this function takes in a file conataining a list of ips and returns a list
            containing all the countries that list of ip spans.
        2. make_whitelist(path_to_file, output_file, subnet), this function generated a zmap whitelist file from an input of ips.
"""

import os
import geoip2.database
reader = geoip2.database.Reader('/home/fatima/Documents/internet_measurements/ark_analysis/geolite_db/GeoLite2-City.mmdb')
reader_asn = geoip2.database.Reader('/home/fatima/Documents/internet_measurements/ark_analysis/geolite_db/GeoLite2-ASN.mmdb')
path_to_file = "./team-1/graphs/ip.txt"

def get_country_of_ip(ip):
    try:
        return (reader.city(ip)).country.name
    except:
        return "$"
def get_ip_owner_ip(ip):
    try:
        return (reader_asn.asn(ip)).autonomous_system_organization
    except:
        return "$"

def find_geo_diversity(path_to_file):
    ip_list = []
    ret_list = set([])
    with open(path_to_file, "rb") as f:
        ip_list = f.read().split("\n")
    for ip in ip_list:
        ret_list.add(get_country_of_ip(ip))
    return list(ret_list)     
def make_whitelist(path_to_file, output_file, subnet):
    ip_list = []
    with open(path_to_file, "rb") as f:
        ip_list = f.read().split("\n")
    with open(output_file, "wb") as f:
        for ip in ip_list:
            f.write(ip + "/{}".format(subnet) + "\n")

make_whitelist(path_to_file, "whitelist.txt", 32)

