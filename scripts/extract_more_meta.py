#!/usr/bin/env python

# Script to extract more metadata
# Chris Cheng 2018

import pydicom
import re
import tarfile
import json
import os.path as path
from optparse import OptionParser, Option
from heudiconv.utils import save_json


def get_opt_parser():
    ### use module docstring for help output
    p = OptionParser()

    p.add_options([
        Option("-o", "--output",
               dest="output", default="files to output json dumps to",
               help="this option takes a single filename to dump json values extracted from dicoms"),


    ])

    return p


def dicom_dump(filename, date):
    dataset = date[1]                                   # get actual DICOM dataset from the tuple provided

    with open(filename, 'r') as fp:                     # open the JSON file provided by the user
        dict = json.load(fp)                            # copy the JSON file's contents into a dict
   
    for f in ['PatientSize', 'PatientWeight', 'PatientAge']:
        dict[f] = getattr(dataset, f)                   # insert into the dict
    
    print(filename);                                    # print the JSON filepath to confirm it was loaded
    save_json(filename, dict, indent=2, pretty=True)    # call heudiconv's save_json function to reload it into the JSON


def get_date_from_dicom_tarball(filename):

    try:
        dataset = pydicom.dcmread(filename)         # read the dicom file
        date = dataset.StudyDate                    # get the date
        
        return (date, dataset)                      # return the date and dataset for later use
    
    except pydicom.errors.InvalidDicomError:        # throw exception if DICOM is invalid
        return "DICOM file cannot be read"


def get_tarball_data(filename, name):
    dicoms = tarfile.open(name, 'r')                # open tarball

    for dcm in dicoms.getmembers():                 # in the first dicom
        file = dicoms.extractfile(dcm)              # extract it

        date = get_date_from_dicom_tarball(file)    # get the date
        dicom_dump(filename, date)                  # call dicom_dump and pass the date as a parameter

        break                                       # call it a day after the first dicom file

    dicoms.close()                                  # close the file


def infer_filename(filename):
    # FUNCTION takes json file and infers where its sourcedata is located by searching directories for dataset_description.json

    dirname = filename                      # initializing name of directory being searched (still includes json file in it)
    directories = split(filename)           # splits filename into each individual directory

    i = 0                                   # initializes counter to ensure loop doesn't break through total # of directories 
    found = False                           # initializes boolean for whether or not dataset_description.json has been found
 
    while i < len(directories):             # while number of directories has not been exhausted
        dirname = path.dirname(dirname)     # cut the .json from the dirname

        ds_identifier = path.join(dirname, "dataset_description.json")   # adds dataset_description.json to the end of the dirname so it can be identified
        
        if path.isfile(ds_identifier):      # checks if dataset_description.json is a file
            found = True                    # if so, change boolean to True and break
            break
        else:
            i += 1                          # otherwise, keep searching the directory above

    if found:
        index = len(dirname)                # get the index of the directory dataset_description.json is found in within the overall filename
        pathname = path.join(dirname, "sourcedata")
        
        for x in range(len(directories)-1):
            pathname = path.join(pathname, directories[x+1])
        
        pathname = pathname[:-5] + ".dicom.tgz"
        return pathname

    else:
        raise ValueError('Path to sourcedata invalid. Check if dicom tarball actually exists.')


def split(pathname):
    
    dirname = pathname
    path_split = []
    
    while True:
        dirname, leaf = path.split(dirname)
        
        if leaf:
            path_split.insert(0, leaf)
            
        else:
            return path_split

if __name__ == '__main__':

    parser = get_opt_parser()                   # load up the parser in order to
    (options, files) = parser.parse_args()      # parse cmdline arguments

    # if options.output:                        # in case options are needed in the future, handle them
    #    files.insert(0, options.output)

    for filename in files:                                      # for each JSON file on the cmdline
        if path.isfile(filename) and filename[-4:] == 'json':   # if the JSON file actually exists,
            name = infer_filename(filename)                     # infer the filename of the dicom tarball from the JSON file provided by the user
            get_tarball_data(filename, name)                    # then get the data from that tarball and dump it into the JSON
        else:
            raise ValueError('JSON file provided does not exist or is not a file.')
