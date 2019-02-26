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
    # use module docstring for help output
    p = OptionParser()

    p.add_options([
        Option("-o", "--output",
               dest="output", default="files to output json dumps to",
               help="this option takes a single filename to dump json values extracted from dicoms"),


    ])

    return p


def run_command(cmd):
    print(cmd)
    # later -- actually run it

def dicom_dump(filename, date):
    dataset = date[1]      
    weight = dataset.PatientWeight 

    with open(filename, 'r') as fp:
        dict = json.load(fp)
    
    dict["PatientWeight"] = weight
    print(filename);
    save_json(filename, dict, indent=2, pretty=True)


def get_date_from_dicom_tarball(filename):
    try:
        dataset = pydicom.dcmread(filename)
        date = dataset.StudyDate
        
        return (date, dataset)
    
    except pydicom.errors.InvalidDicomError:
        return "no extraction"


def convert_tarball(filename, name):
    dicoms = tarfile.open(name, 'r')

    for dcm in dicoms.getmembers():
        file = dicoms.extractfile(dcm)

        date = get_date_from_dicom_tarball(file)
        dicom_dump(filename, date)

        break

    dicoms.close()


def infer_filename(filename):
    string = filename;

    # os.path.spliot(filname)
    list = filename.split("/")
    i = 0
    found = False

    while i < len(list):
        string = path.dirname(string) 
        name = string + "/dataset_description.json"
        
        if path.isfile(name):
            found = True
            break
        else:
            i += 1

    if found:
        pos = len(string)
        pathname = string + "/sourcedata" + filename[pos:-5] + ".dicom.tgz"
        return pathname

    else:
        # raise exception ya dig
        return "bleurgh"

if __name__ == '__main__':
    parser = get_opt_parser()

    (options, files) = parser.parse_args()

    if options.output:
        files.insert(0, options.output)

    for filename in files:
        name = infer_filename(filename)

        convert_tarball(filename, name)
