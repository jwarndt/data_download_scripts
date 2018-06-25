import os
import time
import argparse
import sys
from ftplib import FTP

def _examples():

    sys.exit("""\
    
    # Download PRISM data for mean temperature, at a monthly resolution, from 1950 to 2010.
    prism_download -o /out_dir -tr monthly -v tmean -dr 1950 2010
    
    # Download PRISM data for mean temperature and precipitation, at a daily resolution, from 2010 to 2018.
    prism_download -o /out_dir -tr daily -v tmean ppt -dr 2010 2018
    
    # Download PRISM data for max temperature and precipitation, at a monthly resolution, from 1895 to 2018.
    prism_download -o /out_dir -tr monthly -v tmax ppt -dr 1895 2018
    
    """)

def valid_temporal_resolution(ftp, temporal_resolution):
    # check brute force to see if the temporal resolutions provided by
    # the user are valid
    subdirs = []
    ftp.retrlines("LIST", subdirs.append)
    valid_trs = [n.split(" ")[-1] for n in subdirs]
    if temporal_resolution not in valid_trs:
        print("error: temporal resolution provided " + "[" + str(temporal_resolution) + "] is not valid.")
        print("    valid temporal resolutions are: " + str(valid_trs))
        return False
    return True

def valid_variables(ftp, variables):
    # check brute force to see if the variables provided by
    # the user are valid
    subdirs = []
    ftp.retrlines("LIST", subdirs.append)
    valid_vs = [n.split(" ")[-1] for n in subdirs]
    for v in variables:
        if v not in valid_vs:
            print("error: variables provided are not valid.")
            print("    valid variables are: " + str(valid_vs))
            return False
    return True

def valid_date_range(ftp, date_range):
    # check brute force to see if the temporal resolutions provided by
    # the user are valid
    subdirs = []
    ftp.retrlines("LIST", subdirs.append)
    valid_ds = [n.split(" ")[-1] for n in subdirs]
    for n in [0,1]:
        if str(date_range[n]) not in valid_ds:
            print("error: date range provided is not valid.")
            print("    valid date range must fall between years: " + str(valid_ds[0]) + " and " + str(valid_ds[-1]))
            return False
    return True

def data_download(output_dir, temporal_resolution, variables, date_range):
    ftp = FTP("prism.nacse.org")
    ftp.login()

    if not valid_temporal_resolution(ftp, temporal_resolution): # check validity of the user provided temporal resolutions
        return
    ftp.cwd(temporal_resolution)
    if not valid_variables(ftp, variables): # check validity of the user provided variables
        return

    for folder in variables:
        ftp.cwd(folder)
        if not valid_date_range(ftp, date_range): # check validity of the date_range provided variables
            return
        years = [str(n) for n in range(date_range[0], date_range[1]+1)]
        os.mkdir(os.path.join(output_dir, folder))
        for y in years:
            ftp.cwd(y)
            os.mkdir(os.path.join(output_dir + "/" + folder, y))
            filelist = []
            ftp.retrlines("LIST", filelist.append)
            filenames = [n.split(" ")[-1] for n in filelist]
            for f in filenames:
                ftp.retrbinary("RETR " + f, open(os.path.join(output_dir + "/" + folder + "/" + y, f), "wb").write)
                time.sleep(2) # rest for a little
            print("download complete - " + folder + " " + y)
            ftp.cwd("..")
        print("download complete - variable: " + folder + " all years")
        print("=============================================")
        ftp.cwd("..")
    print("download complete for all variables and years")

def main():

    parser = argparse.ArgumentParser(description="""Script for downloading PRISM data via ftp (http://prism.oregonstate.edu/).
                                                    To download data, specify the variables, temporal resolution (daily, monthly), and the years to download.
                                                    """,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-e', '--examples', dest='examples', action='store_true', help='Show usage examples and exit')
    parser.add_argument('-o', '--output', dest='output', help='The output directory where data will be saved', default=None)
    parser.add_argument('-tr', '--temporal-resolution', dest='temporal_resolution', help='The temporal resolution of the data to download', default="monthly")
    parser.add_argument('-v', '--variables', dest='variables', help='The variables for which data will be downloaded', default=['tmean'], type=str, nargs='+')
    parser.add_argument('-dr', '--date-range', dest='date_range', help='The range of years data will be downloaded for. i.e. the start year and the end year (both inclusive)', default=[1980, 2018], type=int, nargs='+')
    
    args = parser.parse_args()
    
    if args.examples:
        _examples()

    
    print('\nStart date & time --- (%s)\n' % time.asctime(time.localtime(time.time())))
    start_time = time.time()
    
    data_download(args.output,
                  args.temporal_resolution,
                  args.variables,
                  args.date_range)
    
    print('\nEnd data & time -- (%s)\nTotal processing time -- (%.2gs)\n' %
                (time.asctime(time.localtime(time.time())), (time.time() - start_time)))
        
if __name__ == '__main__':
    main()