#!/usr/bin/env python3

# Script to make conversion to bids
# Chris Cheng 2018

import pydicom
import re
import tarfile
import json
from optparse import OptionParser, Option
from heudiconv.utils import save_json


def get_opt_parser():
    # use module docstring for help output
    p = OptionParser()

    p.add_options([
        Option("-f", "--files",
               dest="files", default="takes tarball file with .tgz extension",
               help="this option is compatible with string expansion and takes a tarball file with .tgz extension"),

        Option("-o", "--output",
               dest="output", default="the file to output json dumps to",
               help="this option takes a filename to dump json values extracted from dicoms"),


    ])

    return p


def run_command(cmd):
    print(cmd)
    # later -- actually run it

def dicom_dump(filename, date):
    dataset = date[1]      
    weight = dataset.PatientWeight
    filename = filename.split('/').pop()[:-10]

    path = "QA/sub-qa/ses-{}/func/{}.json".format(date[0], filename)
    print(path);
    with open(path, 'r') as fp:
        dict = json.load(fp)
    
    dict["PatientWeight"] = weight
    save_json(path, dict, pretty=True)


def get_date_from_dicom_tarball(filename):
    try:
        dataset = pydicom.dcmread(filename)
        date = dataset.StudyDate
        
        return (date, dataset)
    
    except pydicom.errors.InvalidDicomError:
        return "no extraction"


def convert_tarball(filename):
    dicoms = tarfile.open(filename, 'r')

    for dcm in dicoms.getmembers():
        file = dicoms.extractfile(dcm)

        date = get_date_from_dicom_tarball(file)
        dicom_dump(filename, date)

        break

    dicoms.close()

if __name__ == '__main__':
    parser = get_opt_parser()

    (options, files) = parser.parse_args()

    for filename in files:
        convert_tarball(filename)
