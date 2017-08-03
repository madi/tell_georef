#!/usr/bin/python

__author__ = "Margherita Di Leo"
__date__   = "Thu Aug 3 2017"

# The purpose of this script is to read the metadata of a series of .jp2 files and
# create a .csv file with the names of the files that are georeferenced and another
# .csv file with the non-georeferenced.
# It uses ExifTool http://owl.phy.queensu.ca/~phil/exiftool/ so you need to install
# it before running the script

import os
import subprocess
import re

# directory in which the files are:
INPUT_FOLDER = "add folder here"
# directory where to write csv files
OUTPUT_FOLDER = "add folder here"

# String to look for in the metadata:
# Projected CS Type               : WGS84 UTM zone 33N
CRS = "WGS84 UTM zone 33N"

def isgeoreferenced(filename, metadata, CRS, georeferenced, nongeoreferenced):
    '''Reads the result of exiftool and decide whether the file is georeferenced
    or not.
    '''
    match = re.search(CRS, metadata)
    if match:
        georeferenced.append(filename)
    else:
        nongeoreferenced.append(filename)

    return georeferenced, nongeoreferenced

def writecsv(folder, lista, filename):

    f = open(folder + os.sep + filename,'w')

    for item in lista:
        f.write(item + '\n')

    f.close()



if __name__ == '__main__':
    # open the folder and creates a list of the .jp2 files
    os.chdir(INPUT_FOLDER)
    lista = os.listdir(INPUT_FOLDER)

    # initialize lists of georeferenced and non-georeferenced files
    georeferenced = []
    nongeoreferenced = []

    for tile in enumerate(lista):
        filename = tile[1]
        cmd = "exiftool " + filename
        proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
        (metadata, err) = proc.communicate()
        # print "program output:", metadata
        georeferenced, nongeoreferenced = isgeoreferenced(filename, \
                                                      metadata, \
                                                      CRS, \
                                                      georeferenced, \
                                                      nongeoreferenced)

    # write output on csv files
    writecsv(OUTPUT_FOLDER, georeferenced, "georef.csv")
    writecsv(OUTPUT_FOLDER, nongeoreferenced, "non_georef.csv")

    print "done"








#
