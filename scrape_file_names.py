import os,urllib2,json
from bs4 import BeautifulSoup
from collections import deque






def filter_a_tags(soup,root):
    child_directories = []
    child_files = []
    for link in soup.find_all('a'):
        if link.text != "Name" and link.text != "Last modified" and link.text != "Size" and link.text != "Description" and link.text != "Parent Directory":
            if "warts.gz" in link["href"]:
                child_files.append(root + link["href"])
            else:
                child_directories.append(root + link["href"])
        
    return child_directories, child_files


def main():
    print "Scraping file names"
    all_links = deque([])
    all_files = deque([])

    root_link = "http://data.caida.org/datasets/topology/ark/ipv4/probe-data/"
    root_page = urllib2.urlopen("http://data.caida.org/datasets/topology/ark/ipv4/probe-data/").read()
    soup = BeautifulSoup(root_page, "html.parser")
    
    child_links, child_files = filter_a_tags(soup,root_link)
    for link in child_links:
        all_links.append(link)
    
    for link in child_files:
        child_links.append(link)
    
    while len(all_links):
        link = all_links.popleft()
        print link
        child_links, child_files = filter_a_tags(BeautifulSoup((urllib2.urlopen(link)),"html.parser"), link)
        for link in child_links:
            all_links.append(link)
    
        for link in child_files:
            child_links.append(link)

    with open("all_files.txt", "wb") as f:
        f.write(json.dumps(all_files))
    
    print all_files
    
    """
    for link in all_links:
        child_links, child_files = filter_a_tags(BeautifulSoup((urllib2.urlopen(link)),"html.parser"), link)
        print child_links, child_files
    """

main()









