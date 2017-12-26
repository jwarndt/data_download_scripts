import os
import time
from ftplib import FTP

destination_directory = "D:/prism_data"

ftp = FTP("prism.nacse.org")
ftp.login()

subdirs = ["tmin","tmean","ppt"]
years = [str(n) for n in range(1981, 2018)] # change range to download different years
ftp.cwd("daily")
start = time.time()
for folder in subdirs:
    ftp.cwd(folder)
    os.mkdir(os.path.join(destination_directory, folder))
    for y in years:
        ftp.cwd(y)
        os.mkdir(os.path.join(destination_directory + "/" + folder, y))
        filelist = []
        ftp.retrlines("LIST", filelist.append)
        filenames = [n.split(" ")[-1] for n in filelist]
        for f in filenames:
            ftp.retrbinary("RETR " + f, open(os.path.join(destination_directory + "/" + folder + "/" + y, f), "wb").write)
            time.sleep(2) # rest for a little
        print("done with year: " + y)
        ftp.cwd("..")
    print("done with folder: " + folder)
    ftp.cwd("..")
print("done")
print("total processing time: " + str(time.time() - start))