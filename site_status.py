#!/usr/bin/python
#*************************************************************************************************************#
#Name: Koteswararao Sakhamuri                                                                                 #
#Date:20/02/2020                                                                                              # 
#Purpose:This script will                                                                                     #
#1. Read file with webpages, path to the file need to be provided as parameter (example file pages.txt)       #
#2. Check if given webpages are responding on port 433 (not ping)                                             #
#3. Log into an output file under /var/log/stats, with information that web was available or Error when       #
#   wasn't - script should allow to choose different path/filename.Let's assume that /var/log/stats will be   #
#   default choice.                                                                                           #
#4. Update csv file with statistics like:                                                                     #
#   ADDRES,STAT                                                                                               #
#   www.google.pl,100%                                                                                        #
#*************************************************************************************************************#
import sys
import os
import socket
import time
import re
import StringIO
import csv

port = 443
default_filepath = '/var/log/stats'

def isReachable(url, port):
    """
    This function reads the URL and port and check if port is open or not
    :argument 1: URL
    :argument 2: PORT
    :return: True/False #status of Port
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
       #checks site avilability
       s.connect((url, int(port)))
       s.shutdown(socket.SHUT_RDWR)
       return True
    except:
       return False
    finally:
       s.close()

def file_exits(file):
    """
    This function reads the file in the given path and pass the URLs to isReachable function
    :argument: file path
    :return: a dirctory with reachability status
    """
    #Reads the file line by line
    Read_file = open(file, 'r')
    count = 0
    results = {}
    while True:
      count += 1
      lines = Read_file.readlines()
      if not lines:
         break
      for line in lines:
          #Extracting sites without special charecters
          url = re.findall(r'^www.[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}', line)
          str_url = str(url[0])
          #Passing site URL to check its avilability
          url_status = isReachable(str_url, port)
          if url_status:
             results[str_url] = "100%"
          else:
             results[str_url] = "0%"
    Read_file.close()
    return results

def update_csv_file(final_result):
    """
    This function writes the result to CSV file in the given path
    :parameter 1: takes dictionary values  
    """
    try:
        File_path = raw_input('Enter path to store results '+default_filepath+' (default): ')
        if len(File_path) > 0 and os.path.exists(File_path):
           with open(os.path.join(File_path, "Sites-Availability-"+str(time.strftime('%Y%m%d%H%M%S'))+'.csv'), "w") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['ADDRESS', 'STATUS'])
                writer.writeheader()
                for key in final_result.keys():
                    writer.writerow({'ADDRESS': key, 'STATUS': final_result[key]})
        else:
             print('Writing to default path.....')
             with open(os.path.join(default_filepath, "Sites-Availability-"+str(time.strftime('%Y%m%d%H%M%S'))+'.csv'), "w") as csvfile:
                  writer = csv.DictWriter(csvfile, fieldnames=['ADDRESS', 'STATUS'])
                  writer.writeheader()
                  for key in final_result.keys():
                      writer.writerow({'ADDRESS': key, 'STATUS': final_result[key]})
     
    except IndexError:
           print('Please provide valid path to save csv file!!!')
           print("USEAGE: Enter path to store results /var/log/stats(default): /path/to/logs-folder")
       
if __name__ == "__main__":
    """
    Script starts here by taking the path to file where URLs exists. If path doest exist it will write to default location
    :parameter 1: Path to file in which URLs are present
    :Example: python py_script2.py /path/to/urls/file.txt
    """
    try:
         #Checks if path is passed as argument and proceeds further
         path = sys.argv[1]
         if os.path.exists(path):
            final_result = file_exits(path)
            #Passing dictionary to write to CSV file
            update_csv_file(final_result)
         else:
            print("File doesn't exist")

    except IndexError:
            #Throws error when file is not passed as argument
            print('Please provide path to URLs file!!!')
            print("USEAGE: python script.py /path/to/urls/file.txt")
