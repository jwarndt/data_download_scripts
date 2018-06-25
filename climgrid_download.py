import os
import time
from ftplib import FTP

"""
script for donwloading NOAA ClimGrid data via ftp
(ftp://ftp.ncdc.noaa.gov/pub/data/climgrid/)
"""

destination_directory = "D:/climgrid"

ftp = FTP("ftp.ncdc.noaa.gov")
ftp.login()

years = [str(n) for n in range(1895, 2018)] # change range to download different years
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
ftp.cwd("pub/data/climgrid")
start = time.time()
filelist = []
ftp.retrlines("LIST", filelist.append) # list directory contents and append them to filelist
filenames = [n.split(" ")[-1] for n in filelist] # file name is 
count = 0 # variable to check up on status of download
for f in filenames:
    ftp.retrbinary("RETR " + f, open(os.path.join(destination_directory, f), "wb").write)
    time.sleep(2) # rest for a little
    count+=1
    if count%12 == 0:
        print("done with year: " + str(count/12))
print("done")
print("total processing time: " + str(time.time() - start))