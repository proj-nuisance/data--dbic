#!/usr/bin/env python3

# Script to make conversion to bids
# Chris Cheng 2018

import dicom as pydicom
import re
import tarfile
from optparse import OptionParser, Option


def get_opt_parser():
    # use module docstring for help output
    p = OptionParser()

    p.add_options([
        Option("-p", "--placeholder",
               dest="hopa", default="leaving room for future options to be added",
               help="out of order"),

    ])

    return p


def run_command(cmd):
    print(cmd)
    # later -- actually run it


def get_date_from_dicom_tarball(filename):
    try:
        dataset = pydicom.read_file(filename)
        date = dataset.StudyDate
        
        return date
    except pydicom.errors.InvalidDicomError:
        return "no extraction"


def get_sid_from_filename(filename):
    # e.g. for Haxby/Sam/1021_actions/sourcedata/sub-sid000416/ses-raiders/anat/sub-sid000416_ses-raiders_T2w.dicom.tgz
    # it would be  sid000416
    if re.search('.*/sub-(?P<sid>sid\d+)/.*', filename):
        sid = re.search('.*/sub-(?P<sid>sid\d+)/.*', filename)
    else:
        sid = re.search('.*/sub-(?P<sid>\w+)/.*', filename)

    return sid.group('sid')


def convert_tarball(filename):
    dicoms = tarfile.open(filename, 'r')

    for dcm in dicoms.getmembers():
        file = dicoms.extractfile(dcm)
        date = get_date_from_dicom_tarball(file)
        subjid = get_sid_from_filename(filename)

        # run the command which does conversion
        run_command('heudiconv --bids -f reproin -s {} -ss {} --files {}'.format(subjid, date, filename))

        break

    dicoms.close()

if __name__ == '__main__':
    parser = get_opt_parser()

    (options, files) = parser.parse_args()

    for filename in files:
        convert_tarball(filename)
